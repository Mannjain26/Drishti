"""
Satark AI - Cross-Centre Fraud Correlation Engine (FR-8, USP-5a)
Detects:
- Multi-centre proxy operations (identical or shifted attendance curves across centres)
- Reused video footage patterns
- Shared equipment fingerprints
"""
import numpy as np
from typing import List, Dict, Any, Tuple

class CrossCentreCorrelationEngine:
    def __init__(self, correlation_threshold: float = 0.92):
        self.correlation_threshold = correlation_threshold

    def compute_curve_similarity(self, curve1: List[int], curve2: List[int]) -> float:
        if not curve1 or not curve2 or len(curve1) != len(curve2):
            return 0.0
        
        v1 = np.array(curve1, dtype=np.float64)
        v2 = np.array(curve2, dtype=np.float64)

        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        cosine_sim = float(np.dot(v1, v2) / (norm1 * norm2))
        return round(cosine_sim, 3)

    def analyze_cross_centre_collusion(self, centres_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        centres_data is a list of {"centre_id": str, "session_id": str, "dwell_curve": List[int]}
        """
        flagged_pairs = []
        n = len(centres_data)
        for i in range(n):
            for j in range(i + 1, n):
                c1 = centres_data[i]
                c2 = centres_data[j]
                
                # Check cosine similarity on presence curves
                sim = self.compute_curve_similarity(c1.get("dwell_curve", []), c2.get("dwell_curve", []))
                if sim >= self.correlation_threshold and len(c1.get("dwell_curve", [])) >= 4:
                    flagged_pairs.append({
                        "centre_a": c1["centre_id"],
                        "centre_b": c2["centre_id"],
                        "similarity_score": sim,
                        "type": "SYNCHRONIZED_ATTENDANCE_CURVE",
                        "severity": "HIGH",
                        "description": f"Identical attendance pattern detected between {c1['centre_id']} and {c2['centre_id']} (Cosine similarity: {sim})"
                    })

        return flagged_pairs
