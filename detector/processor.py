from __future__ import annotations

from typing import Any
from dataclasses import dataclass

try:
    from processing.frame_pipeline import AIFrame, AIProcessor
except ImportError:
    @dataclass
    class AIFrame:
        frame: Any
        frame_id: str = "frame-001"
        camera_id: str = "CAM-01"
        room: str = "Room-101"

    class AIProcessor:
        def process(self, frame: AIFrame) -> dict[str, Any]:
            raise NotImplementedError

from .face_detector import FaceDetector


class FaceDetectionProcessor(AIProcessor):
    """Phase 4 AI processor: local face detection only."""

    def __init__(self, detector: FaceDetector):
        self.detector = detector

    def process(self, frame: AIFrame) -> dict[str, Any]:
        detections = self.detector.detect(frame.frame)
        return {
            "processor": "face_detection",
            "model": "YuNet",
            "frame_id": getattr(frame, "frame_id", "0"),
            "camera_id": getattr(frame, "camera_id", "CAM-01"),
            "room": getattr(frame, "room", "Room-101"),
            "face_count": len(detections),
            "detections": [d.as_dict() for d in detections],
            "inference_latency_ms": round(self.detector.last_inference_ms, 3),
            "model_loaded": self.detector.loaded,
            "error": self.detector.last_error,
        }
