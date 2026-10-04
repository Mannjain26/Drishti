"""
Satark AI - Dwell-Time Accumulator & Session-Presence Curve (FR-2)
Tracks continuous presence curves and detects 'Punch-and-Leave' fraud collapse patterns.
"""
import numpy as np
from typing import List, Dict, Any

class DwellTimeAccumulator:
    def __init__(self, window_size: int = 12, collapse_threshold: float = 0.40):
        self.collapse_threshold = collapse_threshold
        self.timestamps: List[str] = []
        self.headcounts: List[int] = []

    def record_window(self, timestamp: str, count: int):
        self.timestamps.append(timestamp)
        self.headcounts.append(count)

    def compute_summary(self) -> Dict[str, Any]:
        if not self.headcounts:
            return {
                "timestamps": [],
                "headcounts": [],
                "sustained_headcount": 0,
                "peak_headcount": 0,
                "collapse_detected": False,
                "collapse_ratio": 0.0
            }

        counts = np.array(self.headcounts)
        peak_count = int(np.max(counts))
        # Sustained presence = 75th percentile of session counts
        sustained_count = int(np.percentile(counts, 75))

        n_samples = len(counts)
        collapse_detected = False
        collapse_ratio = 0.0

        # Check for Punch-and-Leave Collapse (peak in first 20%, collapse in remaining 80%)
        if n_samples >= 4 and peak_count > 0:
            early_cutoff = max(1, int(n_samples * 0.20))
            early_peak = float(np.max(counts[:early_cutoff]))
            later_median = float(np.median(counts[early_cutoff:]))

            if early_peak > 0:
                collapse_ratio = float((early_peak - later_median) / early_peak)
                if collapse_ratio >= self.collapse_threshold and early_peak >= 5:
                    collapse_detected = True

        return {
            "window_minutes": 5,
            "timestamps": list(self.timestamps),
            "headcounts": [int(c) for c in self.headcounts],
            "sustained_headcount": sustained_count,
            "peak_headcount": peak_count,
            "collapse_detected": collapse_detected,
            "collapse_ratio": round(collapse_ratio, 3)
        }
