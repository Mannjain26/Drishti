import cv2
import threading
import time

class CameraManager:
    """Threaded Camera Manager supporting Webcam, RTSP, Video Files, and Browser Uploads."""
    def __init__(self):
        self.cap = None
        self.is_running = False
        self.current_frame = None
        self.lock = threading.Lock()
        self.thread = None
        self.source_info = {"source_type": "none", "source": ""}
        self.last_browser_frame_time = 0

    def connect(self, source_type: str, source: str) -> bool:
        self.disconnect()
        
        # If browser type, prepare for client-side streaming
        if source_type == "browser":
            self.is_running = True
            self.source_info = {"source_type": "browser", "source": "Browser Webcam"}
            return True

        # Parse device index if device
        src = int(source) if (source_type == "device" and str(source).strip().isdigit()) else source
        
        # Open capture
        try:
            if isinstance(src, int):
                self.cap = cv2.VideoCapture(src, cv2.CAP_DSHOW)
                if not self.cap.isOpened():
                    self.cap = cv2.VideoCapture(src)
            else:
                self.cap = cv2.VideoCapture(src)
        except Exception as e:
            print(f"[Camera Error] {e}")
            return False

        if not self.cap or not self.cap.isOpened():
            return False

        if isinstance(src, int):
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.is_running = True
        self.source_info = {"source_type": source_type, "source": str(source)}
        self.thread = threading.Thread(target=self._capture_worker, daemon=True)
        self.thread.start()
        return True

    def update_browser_frame(self, frame):
        with self.lock:
            self.current_frame = frame
        self.is_running = True
        self.source_info = {"source_type": "browser", "source": "Browser Webcam"}
        self.last_browser_frame_time = time.time()

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
            # Check timeout for browser feed (if no new frame in 4s, clear)
            if self.source_info["source_type"] == "browser" and (time.time() - self.last_browser_frame_time > 4.0):
                self.current_frame = None
                self.is_running = False
            return self.current_frame.copy() if self.current_frame is not None else None

    def disconnect(self):
        self.is_running = False
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
