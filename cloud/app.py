"""
Drishti - Central Cloud Vigilance & AI Vision Backend Server
Provides:
- Real-time AI Face Detection (YuNet) & Recognition (SFace) Live Video Stream
- Camera Stream Management (Webcam / RTSP / Video Files)
- Student Enrollment with 128-D multi-shot face feature embedding
- Live Attendance Tracker & Presence Status
- Ingestion endpoint for signed edge telemetry
- SHA-256 Hash-Chained Alert Ledger API
- SIS ranking & Risk-based audit dispatch queue
- REST API for Web Command Dashboard
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import csv
import io
import json
import time
import os
import cv2
import numpy as np

from schemas.telemetry import TelemetryPayload
from schemas.attendance import AttendanceRecord as SchemaAttendanceRecord
from schemas.bom import SanctionedBOM
from cloud.ledger import HashChainedLedger
from cloud.crosscheck import AttendanceCrossCheckEngine
from cloud.scorer import SISScorer
from cloud.correlation import CrossCentreCorrelationEngine
from edge.packager import TelemetryPackager

# Database & AI Modules
from database import init_db, get_db, Student, AttendanceRecord as DBAttendanceRecord, AttendanceSession, FaceEmbedding
from ai_modules.model_downloader import ensure_models
from ai_modules.camera_manager import CameraManager
from ai_modules.face_detector import FaceDetector
from ai_modules.face_recognizer import SFaceRecognizer
from ai_modules.enrollment import EnrollmentService
from ai_modules.pipeline import FramePipeline

# Root Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# 1. Initialize DB & Models
init_db()
models = ensure_models(MODELS_DIR)

camera_manager = CameraManager()
face_detector = FaceDetector(models["yunet"])
face_recognizer = SFaceRecognizer(models["sface"], distance_threshold=0.45)
pipeline = FramePipeline(camera_manager, face_detector, face_recognizer)

app = FastAPI(title="Drishti Cloud Vigilance & AI Vision Core", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage & vigilance state
ledger = HashChainedLedger()
crosschecker = AttendanceCrossCheckEngine()
scorer = SISScorer()
correlation_engine = CrossCentreCorrelationEngine()
packager = TelemetryPackager()

telemetry_store: Dict[str, List[Dict[str, Any]]] = {}
attendance_store: Dict[str, List[Dict[str, Any]]] = {}
bom_store: Dict[str, Dict[str, Any]] = {}
sis_rankings: Dict[str, Dict[str, Any]] = {}
audit_dispatch_queue: List[Dict[str, Any]] = []

if os.path.exists(DASHBOARD_DIR):
    app.mount("/static", StaticFiles(directory=DASHBOARD_DIR), name="static")

@app.get("/")
def serve_dashboard():
    index_path = os.path.join(DASHBOARD_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "system": "Drishti Vigilance & AI Vision Core",
        "version": "2.0.0",
        "status": "OPERATIONAL"
    }

# ==========================================
# 📹 AI CAMERA & FACE ATTENDANCE ENDPOINTS
# ==========================================

class CameraConnectRequest(BaseModel):
    source_type: str  # "device", "rtsp", or "file"
    source: str       # "0", "rtsp://...", or "path/to/video.mp4"

@app.post("/api/camera/connect")
def connect_camera(req: CameraConnectRequest):
    """Connects camera / stream source in a non-blocking worker thread."""
    success = camera_manager.connect(req.source_type, req.source)
    if not success:
        raise HTTPException(status_code=400, detail=f"Failed to connect to camera source '{req.source}'. Check device index / network stream.")
    return {
        "status": "success",
        "message": f"Successfully connected to {req.source_type.upper()}: {req.source}",
        "source": camera_manager.source_info
    }

@app.post("/api/camera/disconnect")
def disconnect_camera():
    """Disconnects the active camera feed."""
    camera_manager.disconnect()
    return {"status": "success", "message": "Camera disconnected successfully."}

@app.get("/api/camera/stream")
def camera_stream():
    """Returns real-time MJPEG stream with YuNet detection & SFace recognition overlays."""
    return StreamingResponse(
        pipeline.generate_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.post("/api/students/enroll")
async def enroll_student(
    student_id: str = Form(...),
    name: str = Form(...),
    batch: str = Form("Batch-2026-A"),
    images: List[UploadFile] = File(...)
):
    """Enrolls a student by computing average 128-D facial embeddings across uploaded photos."""
    if len(images) == 0:
        raise HTTPException(status_code=400, detail="Please upload at least 1 image.")

    embeddings = []
    for img_file in images:
        contents = await img_file.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            continue

        faces = face_detector.detect(frame)
        if len(faces) > 0:
            emb = face_recognizer.align_and_extract(frame, faces[0])
            embeddings.append(emb)

    if len(embeddings) == 0:
        raise HTTPException(
            status_code=400,
            detail="No clear face detected in the uploaded images. Please ensure good lighting and clear frontal angle."
        )

    saved = EnrollmentService.enroll_student(student_id.strip(), name.strip(), batch.strip(), embeddings)
    if not saved:
        raise HTTPException(status_code=500, detail="Database error occurred while saving student profile.")

    # Invalidate pipeline cache so new student is instantly recognized
    pipeline.refresh_known_embeddings(force=True)

    return {
        "status": "success",
        "message": f"Successfully enrolled {name} (ID: {student_id}) with {len(embeddings)} facial reference frames.",
        "student_id": student_id,
        "name": name,
        "batch": batch,
        "faces_processed": len(embeddings)
    }

@app.get("/api/attendance/status")
def get_live_attendance_status():
    """Poll endpoint: returns real-time faces detected in camera and presence count."""
    return {
        "active_session": pipeline.active_session_id,
        "camera_connected": camera_manager.is_running,
        "source": camera_manager.source_info,
        "present_count": len(pipeline.currently_present),
        "present_students": list(pipeline.currently_present.values())
    }

@app.get("/api/attendance/history")
def get_attendance_history(db: Session = Depends(get_db)):
    """Returns recent persistent attendance timestamps from SQLite."""
    records = db.query(DBAttendanceRecord, Student).join(
        Student, DBAttendanceRecord.student_id == Student.student_id
    ).order_by(DBAttendanceRecord.timestamp.desc()).limit(100).all()

    return [
        {
            "id": r.AttendanceRecord.id,
            "student_id": r.Student.student_id,
            "name": r.Student.name,
            "batch": r.Student.batch,
            "session_id": r.AttendanceRecord.session_id,
            "timestamp": r.AttendanceRecord.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "status": r.AttendanceRecord.status
        }
        for r in records
    ]

@app.get("/api/students")
def get_all_enrolled_students(db: Session = Depends(get_db)):
    """Returns list of all enrolled students in the database."""
    students = db.query(Student).all()
    return [
        {
            "student_id": s.student_id,
            "name": s.name,
            "batch": s.batch,
            "created_at": s.created_at.strftime("%Y-%m-%d %H:%M:%S") if s.created_at else "",
            "has_embedding": len(s.embeddings) > 0
        }
        for s in students
    ]

@app.delete("/api/students/{student_id}")
def delete_student(student_id: str, db: Session = Depends(get_db)):
    """Deletes an enrolled student and their biometric embeddings."""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    db.delete(student)
    db.commit()
    pipeline.refresh_known_embeddings(force=True)
    return {"status": "success", "message": f"Student {student_id} deleted."}


# ==========================================
# 🛡️ DRISHTI VIGILANCE CORE TELEMETRY & LEDGER
# ==========================================

@app.post("/api/telemetry")
def receive_telemetry(payload: TelemetryPayload):
    telemetry_dict = payload.model_dump()
    
    # Verify cryptographic signature
    if not packager.verify_signature(dict(telemetry_dict)):
        raise HTTPException(status_code=401, detail="Invalid telemetry cryptographic signature! Tampered edge payload.")

    centre_id = payload.centre_id
    if centre_id not in telemetry_store:
        telemetry_store[centre_id] = []
    telemetry_store[centre_id].append(telemetry_dict)

    # 1. Feed Integrity Evaluation
    feed_status = payload.feed_health.status
    feed_tamper_count = 1 if feed_status in ["BLACKOUT", "FROZEN", "COVERED", "OFFLINE"] else 0
    if feed_tamper_count > 0:
        ledger.append_alert(
            centre_id=centre_id,
            session_id=payload.session_id,
            alert_type=f"FEED_INTEGRITY_{feed_status}",
            severity="CRITICAL" if feed_status == "BLACKOUT" else "HIGH",
            description=f"Feed anomaly detected: {feed_status}",
            details={"feed_health": payload.feed_health.model_dump()}
        )

    # 2. Attendance Cross-Check
    reported_count = payload.reported_attendance or 0
    if centre_id in attendance_store:
        for att in attendance_store[centre_id]:
            if att.get("batch_session_id") == payload.session_id:
                reported_count = att.get("reported_attendance_count", reported_count)
                break

    cross_res = crosschecker.cross_check(reported_count, payload.estimated_attendance)
    
    if cross_res["alert_triggered"]:
        ledger.append_alert(
            centre_id=centre_id,
            session_id=payload.session_id,
            alert_type=f"ATTENDANCE_DISCREPANCY_{cross_res['alert_level']}",
            severity="CRITICAL" if cross_res["alert_level"] == "CRITICAL" else "MEDIUM",
            description=cross_res["message"],
            details=cross_res
        )

    # Dwell Collapse Check
    if payload.dwell_curve_summary.collapse_detected:
        ledger.append_alert(
            centre_id=centre_id,
            session_id=payload.session_id,
            alert_type="PUNCH_AND_LEAVE_SUSPECTED",
            severity="HIGH",
            description="Steep headcount collapse detected shortly after session start.",
            details=payload.dwell_curve_summary.model_dump()
        )

    # 3. Compute SIS
    eq_status_list = [item.model_dump() for item in payload.equipment_status]
    sis_result = scorer.compute_sis(
        attendance_penalty_ratio=cross_res["penalty_ratio"],
        feed_tamper_count=feed_tamper_count,
        equipment_statuses=eq_status_list,
        trainer_present=payload.trainer_present,
        collusion_detected=False
    )

    sis_rankings[centre_id] = {
        "centre_id": centre_id,
        "last_session_id": payload.session_id,
        "timestamp": payload.timestamp,
        "sis_score": sis_result["sis_score"],
        "risk_tier": sis_result["risk_tier"],
        "audit_recommended": sis_result["audit_recommended"],
        "penalties": sis_result["penalties"],
        "flags": sis_result["flags"],
        "estimated_attendance": payload.estimated_attendance,
        "reported_attendance": reported_count,
        "discrepancy_pct": cross_res["discrepancy_pct"],
        "feed_health": payload.feed_health.status,
        "trainer_present": payload.trainer_present
    }

    # If high risk, add to audit queue
    if sis_result["audit_recommended"]:
        if not any(a["centre_id"] == centre_id for a in audit_dispatch_queue):
            audit_dispatch_queue.append({
                "centre_id": centre_id,
                "session_id": payload.session_id,
                "score": sis_result["sis_score"],
                "reason": "Low SIS score / Critical vigilance alerts",
                "dispatched": False,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            })

    return {
        "status": "PROCESSED",
        "centre_id": centre_id,
        "sis_score": sis_result["sis_score"],
        "risk_tier": sis_result["risk_tier"]
    }

@app.post("/api/attendance/upload")
async def upload_attendance_csv(file: UploadFile = File(...)):
    contents = await file.read()
    decoded = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))
    
    count = 0
    for row in reader:
        c_id = row["centre_id"]
        if c_id not in attendance_store:
            attendance_store[c_id] = []
        
        record = {
            "centre_id": c_id,
            "batch_session_id": row["batch_session_id"],
            "date": row["date"],
            "scheduled_start": row["scheduled_start"],
            "scheduled_end": row["scheduled_end"],
            "reported_attendance_count": int(row["reported_attendance_count"]),
            "course_name": row.get("course_name", "Skilling"),
            "trainer_name": row.get("trainer_name", "Instructor")
        }
        attendance_store[c_id].append(record)
        count += 1

    return {"status": "SUCCESS", "records_imported": count}

@app.get("/api/centres/ranking")
def get_centre_rankings():
    rankings_list = sorted(list(sis_rankings.values()), key=lambda x: x["sis_score"])
    return {"centres": rankings_list}

@app.get("/api/ledger")
def get_ledger(centre_id: Optional[str] = None):
    if centre_id:
        return {"alerts": ledger.get_centre_alerts(centre_id)}
    return {"alerts": ledger.chain}

@app.get("/api/ledger/verify")
def verify_ledger():
    valid, err_idx, msg = ledger.verify_integrity()
    return {
        "is_valid": valid,
        "corrupted_block_index": err_idx,
        "message": msg,
        "total_blocks": len(ledger.chain)
    }

@app.get("/api/audit-dispatch")
def get_audit_dispatch():
    return {"queue": audit_dispatch_queue}

@app.post("/api/audit-dispatch/{centre_id}/dispatch")
def dispatch_audit(centre_id: str):
    for item in audit_dispatch_queue:
        if item["centre_id"] == centre_id:
            item["dispatched"] = True
            item["dispatched_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            return {"status": "DISPATCHED", "centre_id": centre_id}
    raise HTTPException(status_code=404, detail="Centre not found in audit queue")
