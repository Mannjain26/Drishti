import cv2
import threading
import time
import numpy as np

class CameraManager:
    """Threaded Camera Manager supporting Webcams, RTSP, Video Files, Browser Streaming, and Cloud Simulation."""
    def __init__(self):
        self.cap = None
        self.is_running = False
        self.current_frame = None
        self.lock = threading.Lock()
        self.thread = None
        self.source_info = {"source_type": "none", "source": ""}
        self.last_browser_frame_time = 0
        self.is_simulation = False

    def connect(self, source_type: str, source: str) -> bool:
        self.disconnect()
        
        # 1. Browser Webcam Mode
        if source_type == "browser":
            self.is_running = True
            self.is_simulation = False
            self.source_info = {"source_type": "browser", "source": "Browser Webcam"}
            return True

        # 2. Local Device Index (e.g. 0)
        src = int(source) if (source_type == "device" and str(source).strip().isdigit()) else source
        
        # Try opening physical camera
        opened = False
        try:
            if isinstance(src, int):
                self.cap = cv2.VideoCapture(src, cv2.CAP_DSHOW)
                if not self.cap.isOpened():
                    self.cap = cv2.VideoCapture(src)
                if self.cap and self.cap.isOpened():
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    opened = True
            else:
                self.cap = cv2.VideoCapture(src)
                if self.cap and self.cap.isOpened():
                    opened = True
        except Exception as e:
            print(f"[Camera Error] {e}")

        # If running on cloud server with no physical camera attached, switch to Cloud Simulation
        if not opened:
            if source_type == "device" or source == "0":
                print("[Camera] No physical USB camera detected on cloud server. Activating Cloud CCTV Simulator mode.")
                self.is_running = True
                self.is_simulation = True
                self.source_info = {"source_type": "simulation", "source": "Cloud CCTV Simulator (Auto-Fallback)"}
                self.thread = threading.Thread(target=self._simulation_worker, daemon=True)
                self.thread.start()
                return True
            else:
                return False

        self.is_running = True
        self.is_simulation = False
        self.source_info = {"source_type": source_type, "source": str(source)}
        self.thread = threading.Thread(target=self._capture_worker, daemon=True)
        self.thread.start()
        return True

    def update_browser_frame(self, frame):
        with self.lock:
            self.current_frame = frame
        self.is_running = True
        self.is_simulation = False
        self.source_info = {"source_type": "browser", "source": "Browser Webcam"}
        self.last_browser_frame_time = time.time()

    def _simulation_worker(self):
        """Generates real-time synthetic classroom training video frames for cloud environments."""
        tick = 0
        while self.is_running and self.is_simulation:
            tick += 1
            # Create synthetic classroom
            frame = np.full((480, 640, 3), (235, 240, 245), dtype=np.uint8)
            
            # Classroom floor & podium
            cv2.rectangle(frame, (0, 300), (640, 480), (180, 195, 210), -1)
            cv2.rectangle(frame, (20, 160), (220, 260), (100, 130, 160), -1) # Smart board
            cv2.putText(frame, "PMKVY SKILL CENTRE - LAB A", (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

            # Simulated moving trainees
            cx1 = int(320 + np.sin(tick * 0.05) * 30)
            cy1 = 280
            cv2.circle(frame, (cx1, cy1 - 40), 24, (200, 160, 140), -1) # Head
            cv2.ellipse(frame, (cx1, cy1 + 25), (35, 45), 0, 0, 360, (50, 120, 200), -1) # Torso

            cx2 = int(480 + np.cos(tick * 0.04) * 20)
            cy2 = 300
            cv2.circle(frame, (cx2, cy2 - 40), 22, (190, 150, 130), -1)
            cv2.ellipse(frame, (cx2, cy2 + 25), (32, 40), 0, 0, 360, (40, 160, 80), -1)

            # Watermark
            cv2.putText(frame, "CLOUD CCTV SIMULATOR ACTIVE", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (60, 60, 180), 2)
            cv2.putText(frame, "Click 'Start Laptop Camera' above for your real webcam", (20, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (100, 100, 100), 1)

            with self.lock:
                self.current_frame = frame
            time.sleep(0.05)

    def _capture_worker(self):
        while self.is_running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret and frame is not None:
                with self.lock:
                    self.current_frame = frame
            else:
                if self.source_info["source_type"] == "file":
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                time.sleep(0.02)
            time.sleep(0.01)

    def get_frame(self):
        with self.lock:
            if self.source_info["source_type"] == "browser" and (time.time() - self.last_browser_frame_time > 4.0):
                self.current_frame = None
                self.is_running = False
            return self.current_frame.copy() if self.current_frame is not None else None

    def disconnect(self):
        self.is_running = False
        self.is_simulation = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=0.8)
        if self.cap:
            try:
                self.cap.release()
            except Exception:
                pass
            self.cap = None
        with self.lock:
            self.current_frame = None
        self.source_info = {"source_type": "none", "source": ""}
