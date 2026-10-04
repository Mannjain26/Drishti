import cv2
import numpy as np
import os

class FaceDetector:
    """YuNet ONNX Face Detector: returns bboxes, confidences, and 5 facial landmarks."""
    def __init__(self, model_path: str, score_threshold: float = 0.6, nms_threshold: float = 0.3):
        self.model_path = model_path
        self.score_threshold = score_threshold
        self.nms_threshold = nms_threshold
        self.detector = None
        self._current_size = (320, 320)
        self._init_detector()

    def _init_detector(self):
        if os.path.exists(self.model_path):
            try:
                self.detector = cv2.FaceDetectorYN.create(
                    model=self.model_path,
                    config="",
                    input_size=self._current_size,
                    score_threshold=self.score_threshold,
                    nms_threshold=self.nms_threshold,
                    top_k=50
                )
            except Exception as e:
                print(f"[YuNet Init Warning] {e}")

    def detect(self, image: np.ndarray):
        if self.detector is None:
            self._init_detector()
            if self.detector is None:
                return []

        h, w, _ = image.shape
        if (w, h) != self._current_size:
            self.detector.setInputSize((w, h))
            self._current_size = (w, h)
        
        try:
            _, faces = self.detector.detect(image)
            return faces if faces is not None else []
        except Exception as e:
            print(f"[YuNet Detection Error] {e}")
            return []
