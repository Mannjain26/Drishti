"""
Satark AI - Universal Frame Ingestion Module (L0)
Ingests:
- RTSP / IP CCTV streams
- Local MP4 / AVI video files
- Periodic JPEG snapshots
- Synthetic frame simulator for test automation & Red-Team verification
"""
import cv2
import numpy as np
import time
from typing import Generator, Optional, Tuple

class FrameIngestor:
    def __init__(self, source: Optional[str] = None, fps_target: float = 2.0):
        self.source = source
        self.fps_target = fps_target
        self.cap = None

    def open_stream(self):
        if self.source is not None:
            self.cap = cv2.VideoCapture(self.source)

    def read_frames(self, max_frames: int = 100) -> Generator[np.ndarray, None, None]:
        frame_delay = 1.0 / self.fps_target
        if self.cap is not None and self.cap.isOpened():
            count = 0
            while count < max_frames:
                ret, frame = self.cap.read()
                if not ret:
                    break
                # Downscale to 480p standard as per SRS C2 / NFR-3
                h, w = frame.shape[:2]
                if h > 480:
                    scale = 480.0 / h
                    frame = cv2.resize(frame, (int(w * scale), 480))
                yield frame
                count += 1
                time.sleep(frame_delay)
            self.cap.release()
        else:
            # Fallback to simulated clean classroom frame generator
            for i in range(max_frames):
                yield self.generate_simulated_frame(num_persons=18, is_blackout=False, has_trainer=True)
                time.sleep(0.01)

    @staticmethod
    def generate_simulated_frame(num_persons: int = 15,
                                  is_blackout: bool = False,
                                  is_covered: bool = False,
                                  has_trainer: bool = True,
                                  equipment_present: bool = True) -> np.ndarray:
        """
        Creates visually rich synthetic training classroom frames for validation.
        """
        if is_blackout:
            return np.zeros((480, 640, 3), dtype=np.uint8)
        if is_covered:
            return np.full((480, 640, 3), (240, 240, 240), dtype=np.uint8)

        # Classroom background
        frame = np.full((480, 640, 3), (220, 225, 230), dtype=np.uint8)
        
        # Floor & Wall line
        cv2.line(frame, (0, 150), (640, 150), (180, 180, 180), 2)
        cv2.putText(frame, "DRISHTI - CCTV FEED MONITOR [LIVE]", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 50), 2)

        # Trainer podium (Instructor Zone: left region 0 to 200px)
        cv2.rectangle(frame, (30, 200), (150, 350), (160, 140, 120), -1)
        cv2.putText(frame, "PODIUM", (45, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        if has_trainer:
            # Draw Instructor
            cv2.circle(frame, (90, 160), 22, (200, 180, 160), -1)  # Face
            cv2.rectangle(frame, (65, 185), (115, 300), (80, 40, 20), -1) # Body
            cv2.putText(frame, "TRAINER", (65, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 100, 0), 1)

        # Workbenches / PCs
        if equipment_present:
            for bx in [220, 360, 500]:
                cv2.rectangle(frame, (bx, 280), (bx + 100, 380), (100, 110, 120), -1) # Workbench
                cv2.rectangle(frame, (bx + 20, 230), (bx + 80, 280), (40, 40, 40), -1) # PC Monitor
                cv2.putText(frame, "PC", (bx + 40, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        # Draw Trainees
        np.random.seed(42)
        cols = 5
        for i in range(num_persons):
            col_idx = i % cols
            row_idx = i // cols
            tx = 220 + col_idx * 80 + np.random.randint(-10, 10)
            ty = 300 + row_idx * 50 + np.random.randint(-5, 5)
            if tx < 620 and ty < 460:
                cv2.circle(frame, (tx, ty - 30), 15, (210, 190, 170), -1) # Face
                cv2.rectangle(frame, (tx - 15, ty - 15), (tx + 15, ty + 30), (140, 70, 50), -1) # Torso

        return frame
