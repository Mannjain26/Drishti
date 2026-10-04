"""
Satark AI - Anonymous Person Detection & Tracking Engine (FR-1, FR-7)
Performs:
- Anonymous headcount per frame/window
- Bounding-box tracking for movement & dwell accumulation
- Trainer role-pattern detection in instructional zone
- ZERO facial identification or biometric storage
"""
import cv2
import numpy as np
from typing import List, Dict, Any, Tuple

class AnonymousDetector:
    def __init__(self, model_name: str = "yolov8n.pt", confidence_thresh: float = 0.35):
        self.confidence_thresh = confidence_thresh
        self.yolo_model = None
        
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        
        # Try loading YOLOv8 if ultralytics is present and model exists locally
        try:
            import os
            if os.path.exists(model_name):
                from ultralytics import YOLO
                self.yolo_model = YOLO(model_name)
        except Exception as e:
            pass

    def detect_persons(self, frame: np.ndarray, instructor_roi: Tuple[float, float, float, float] = (0.0, 0.0, 0.4, 1.0)) -> Dict[str, Any]:
        """
        Detects persons anonymously on privacy-blurred frame.
        instructor_roi is (norm_x1, norm_y1, norm_x2, norm_y2) for podium/board area.
        
        Returns:
            headcount: int
            boxes: List of [x1, y1, x2, y2, confidence]
            trainer_detected: bool
        """
        if frame is None or frame.size == 0:
            return {"headcount": 0, "boxes": [], "trainer_detected": False}

        h, w = frame.shape[:2]
        boxes = []
        trainer_detected = False
        
        # Instructor zone coordinates
        inst_x1, inst_y1 = int(instructor_roi[0] * w), int(instructor_roi[1] * h)
        inst_x2, inst_y2 = int(instructor_roi[2] * w), int(instructor_roi[3] * h)

        if self.yolo_model is not None:
            try:
                results = self.yolo_model(frame, classes=[0], conf=self.confidence_thresh, verbose=False)
                for r in results:
                    for box in r.boxes:
                        coords = box.xyxy[0].cpu().numpy().tolist()
                        conf = float(box.conf[0].cpu().numpy())
                        x1, y1, x2, y2 = [int(v) for v in coords]
                        boxes.append([x1, y1, x2, y2, conf])
                        
                        # Check if person center falls in instructor zone
                        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                        if inst_x1 <= cx <= inst_x2 and inst_y1 <= cy <= inst_y2:
                            trainer_detected = True
            except Exception as ex:
                boxes = self._fallback_hog(frame)
        else:
            boxes = self._fallback_hog(frame)

        # Check trainer in fallback
        if not trainer_detected and len(boxes) > 0:
            for b in boxes:
                cx, cy = (b[0] + b[2]) // 2, (b[1] + b[3]) // 2
                if inst_x1 <= cx <= inst_x2 and inst_y1 <= cy <= inst_y2:
                    trainer_detected = True
                    break

        return {
            "headcount": len(boxes),
            "boxes": boxes,
            "trainer_detected": trainer_detected
        }

    def _fallback_hog(self, frame: np.ndarray) -> List[List[Any]]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects, weights = self.hog.detectMultiScale(gray, winStride=(8, 8), padding=(8, 8), scale=1.05)
        boxes = []
        for (x, y, w, h), weight in zip(rects, weights):
            if weight > 0.2:
                boxes.append([x, y, x + w, y + h, float(weight)])
        return boxes
