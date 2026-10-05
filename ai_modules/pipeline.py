import cv2
import time
import numpy as np
import datetime
from database import SessionLocal, FaceEmbedding, Student, AttendanceRecord, AttendanceSession
from detector.attendance import AttendanceStore
from detector.face_detector import FaceDetection

class FramePipeline:
    def __init__(self, camera_mgr, detector, recognizer, attendance_db_path="data/detector_attendance.db"):
        self.camera_mgr = camera_mgr
        self.detector = detector
        self.recognizer = recognizer
        self.active_session_id = "SESSION-LIVE-01"
        self.currently_present = {}  # {student_id: {"name": str, "timestamp": str, "confidence": float, "batch": str}}
        self._cached_embeddings = {}
        self._last_db_refresh = 0
        self.attendance_store = AttendanceStore(attendance_db_path)
        
        # Initialize default classroom, batch, and active session in detector AttendanceStore
        try:
            self.attendance_store.upsert_classroom("CLASS-01", "Lab Room 101", "101")
            self.attendance_store.upsert_batch("BATCH-01", "Batch-2026-A")
            active = self.attendance_store.active_session_for_camera("CAM-01")
            if not active:
                today = datetime.date.today().isoformat()
                sess = self.attendance_store.create_session("CLASS-01", "BATCH-01", today, "09:00", "18:00", "CAM-01")
                self.local_session = self.attendance_store.start_session(sess["id"])
            else:
                self.local_session = active
        except Exception as e:
            print(f"[AttendanceStore Init Warning] {e}")
            self.local_session = None

    def refresh_known_embeddings(self, force=False):
        if not force and (time.time() - self._last_db_refresh < 4.0 and self._cached_embeddings):
            return
        
        db = SessionLocal()
        try:
            records = db.query(FaceEmbedding, Student).join(Student, FaceEmbedding.student_id == Student.student_id).all()
            self._cached_embeddings = {
                rec.FaceEmbedding.student_id: (
                    rec.Student.name,
                    np.array(rec.FaceEmbedding.get_vector(), dtype=np.float32),
                    rec.Student.batch
                )
                for rec in records
            }
            self._last_db_refresh = time.time()
        except Exception as e:
            print(f"[Pipeline Cache Refresh Error] {e}")
        finally:
            db.close()

    def record_attendance(self, student_id: str, confidence: float = 0.95):
        if not student_id or student_id == "unknown":
            return

        # 1. Record into local SQLite AttendanceStore (detector/attendance.py)
        try:
            if self.local_session:
                self.attendance_store.mark_present(
                    session_id=self.local_session["id"],
                    student_id=student_id,
                    confidence=confidence,
                    camera_id="CAM-01"
                )
        except Exception as e:
            pass

        # 2. Record into Cloud / Supabase PostgreSQL DB
        db = SessionLocal()
        try:
            session = db.query(AttendanceSession).filter(AttendanceSession.session_id == self.active_session_id).first()
            if not session:
                session = AttendanceSession(session_id=self.active_session_id, classroom="Room-101")
                db.add(session)
                db.commit()

            # Record if not recorded within the last 60 seconds
            cutoff = datetime.datetime.utcnow() - datetime.timedelta(seconds=60)
            recent = db.query(AttendanceRecord).filter(
                AttendanceRecord.session_id == self.active_session_id,
                AttendanceRecord.student_id == student_id,
                AttendanceRecord.timestamp >= cutoff
            ).first()

            if not recent:
                att = AttendanceRecord(
                    session_id=self.active_session_id,
                    student_id=student_id,
                    timestamp=datetime.datetime.utcnow(),
                    status="Present"
                )
                db.add(att)
                db.commit()
        except Exception as e:
            db.rollback()
            print(f"[Pipeline Attendance Record Error] {e}")
        finally:
            db.close()

    def match_face(self, feature: np.ndarray, threshold: float = 0.55):
        """Matches a 128-D feature vector against enrolled student embeddings using cosine similarity."""
        if feature is None or len(self._cached_embeddings) == 0:
            return "unknown", "Unknown", 0.0, 1.0

        best_sid = "unknown"
        best_name = "Unknown"
        best_sim = -1.0

        for sid, (name, emb, batch) in self._cached_embeddings.items():
            if emb is None or len(emb) == 0:
                continue
            # Cosine similarity between L2-normalized vectors
            sim = float(np.dot(feature, emb))
            if sim > best_sim:
                best_sim = sim
                best_sid = sid
                best_name = name

        if best_sim >= threshold:
            distance = max(0.0, 1.0 - best_sim)
            return best_sid, best_name, best_sim, distance
        return "unknown", "Unknown", max(0.0, best_sim), max(0.0, 1.0 - best_sim)

    def generate_stream(self):
        while True:
            frame = self.camera_mgr.get_frame()
            if frame is None:
                # High-tech Cyber / Vigilance "Awaiting Stream" visual
                blank = np.zeros((480, 640, 3), dtype=np.uint8)
                blank[:] = (18, 14, 10)  # Dark sleek background
                
                # Draw subtle grid
                for y in range(0, 480, 40):
                    cv2.line(blank, (0, y), (640, y), (30, 25, 20), 1)
                for x in range(0, 640, 40):
                    cv2.line(blank, (x, 0), (x, 480), (30, 25, 20), 1)

                cv2.putText(blank, "DRISHTI AI VISION FEED", (150, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 215, 255), 2)
                cv2.putText(blank, "CAMERA OFFLINE / DISCONNECTED", (135, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 240), 2)
                cv2.putText(blank, "Connect webcam (0) or RTSP stream above", (130, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (160, 160, 160), 1)
                
                _, jpeg = cv2.imencode('.jpg', blank, [cv2.IMWRITE_JPEG_QUALITY, 80])
                yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
                time.sleep(0.1)
                continue

            self.refresh_known_embeddings()
            
            # Detect faces using detector.FaceDetector
            detections = self.detector.detect(frame)
            detected_now = {}

            # Visual overlay timestamp & watermark
            h, w, _ = frame.shape
            cv2.rectangle(frame, (0, 0), (w, 35), (15, 15, 20), -1)
            cv2.putText(
                frame,
                f"DRISHTI LIVE AI (DETECTOR) | FACES: {len(detections)} | {time.strftime('%Y-%m-%d %H:%M:%S')}",
                (12, 24),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 200),
                2
            )

            for det in detections:
                if isinstance(det, FaceDetection):
                    fx, fy, fw, fh = det.x, det.y, det.width, det.height
                    score = det.confidence
                    model_row = det.model_row
                    track_id = det.track_id
                else:
                    fx, fy, fw, fh = map(int, det[0:4])
                    score = float(det[14])
                    model_row = det
                    track_id = None

                if model_row is None:
                    continue

                # Extract 128-D SFace embedding using detector.SFaceRecognizer
                try:
                    embedding = self.recognizer.extract(frame, model_row)
                except Exception:
                    continue

                student_id, name, sim, dist = self.match_face(embedding)

                is_recognized = (student_id != "unknown")
                box_color = (0, 230, 115) if is_recognized else (50, 50, 240)  # Green vs Red
                confidence = sim if is_recognized else score
                
                track_tag = f" [#{track_id}]" if track_id else ""
                label = f"{name}{track_tag} ({confidence*100:.1f}%)" if is_recognized else f"Unknown ({score*100:.0f}%)"

                # Draw bounding box with rounded corner accents
                cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), box_color, 2)
                
                # Corner tick marks
                cl = min(20, max(5, fw // 4), max(5, fh // 4))
                cv2.line(frame, (fx, fy), (fx + cl, fy), (255, 255, 255), 2)
                cv2.line(frame, (fx, fy), (fx, fy + cl), (255, 255, 255), 2)
                cv2.line(frame, (fx + fw, fy), (fx + fw - cl, fy), (255, 255, 255), 2)
                cv2.line(frame, (fx + fw, fy), (fx + fw, fy + cl), (255, 255, 255), 2)

                # Label tag
                (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
                cv2.rectangle(frame, (fx, max(0, fy - 26)), (fx + tw + 10, max(26, fy)), box_color, -1)
                cv2.putText(
                    frame,
                    label,
                    (fx + 5, max(18, fy - 7)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 0, 0),
                    2
                )

                # 5 Facial Landmarks (Eyes, Nose, Mouth Corners)
                if len(model_row) >= 14:
                    landmarks = np.asarray(model_row[4:14], dtype=np.float32).reshape((5, 2)).astype(int)
                    for (lx, ly) in landmarks:
                        cv2.circle(frame, (lx, ly), 2, (0, 255, 255), -1)

                if is_recognized:
                    self.record_attendance(student_id, confidence=confidence)
                    batch_name = self._cached_embeddings.get(student_id, ("", None, "General"))[2]
                    detected_now[student_id] = {
                        "student_id": student_id,
                        "name": name,
                        "batch": batch_name,
                        "confidence": round(float(confidence), 3),
                        "distance": round(float(dist), 3),
                        "timestamp": time.strftime("%H:%M:%S")
                    }

            self.currently_present = detected_now

            # Encode as JPEG
            _, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 82])
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            time.sleep(0.03)  # ~30 FPS
