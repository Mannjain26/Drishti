import cv2
import numpy as np
import os

class SFaceRecognizer:
    """SFace ONNX Face Recognizer: extracts 128-D features and computes cosine similarity."""
    def __init__(self, model_path: str, distance_threshold: float = 0.45):
        self.model_path = model_path
        self.threshold = distance_threshold
        self.recognizer = None
        self._init_recognizer()

    def _init_recognizer(self):
        if os.path.exists(self.model_path):
            try:
                self.recognizer = cv2.FaceRecognizerSF.create(model=self.model_path, config="")
            except Exception as e:
                print(f"[SFace Init Warning] {e}")

    def align_and_extract(self, frame: np.ndarray, face_data: np.ndarray) -> np.ndarray:
        if self.recognizer is None:
            self._init_recognizer()
            if self.recognizer is None:
                return np.zeros((128,), dtype=np.float32)

        try:
            aligned_face = self.recognizer.alignCrop(frame, face_data)
            feature = self.recognizer.feature(aligned_face)
            norm = np.linalg.norm(feature)
            if norm > 0:
                return (feature.flatten() / norm).astype(np.float32)
            return feature.flatten().astype(np.float32)
        except Exception as e:
            print(f"[SFace Feature Error] {e}")
            return np.zeros((128,), dtype=np.float32)

    def compute_cosine_distance(self, feat1: np.ndarray, feat2: np.ndarray) -> float:
        """Returns Cosine Distance (0 = Identical, 1 = Orthogonal, 2 = Opposite)."""
        f1 = np.asarray(feat1, dtype=np.float32)
        f2 = np.asarray(feat2, dtype=np.float32)
        norm1 = np.linalg.norm(f1)
        norm2 = np.linalg.norm(f2)
        if norm1 == 0 or norm2 == 0:
            return 1.0
        similarity = float(np.dot(f1, f2) / (norm1 * norm2))
        return max(0.0, 1.0 - similarity)

    def match(self, target_embedding: np.ndarray, known_embeddings: dict) -> tuple:
        """
        known_embeddings: {student_id: (name, np_embedding)}
        Returns: (student_id, name, min_distance) or ("unknown", "Unknown", min_dist)
        """
        best_match_id = "unknown"
        best_name = "Unknown"
        min_dist = 10.0

        for sid, (name, emb) in known_embeddings.items():
            dist = self.compute_cosine_distance(target_embedding, emb)
            if dist < min_dist:
                min_dist = dist
                if dist <= self.threshold:
                    best_match_id = sid
                    best_name = name

        return best_match_id, best_name, min_dist
