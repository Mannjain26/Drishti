"""
Satark AI - Attendance Cross-Check Engine (FR-13, §6.5, §8.2)
Compares camera-derived anonymous attendance against centre-submitted attendance records.
Maintains strict separation between:
1. AI-estimated physical presence
2. Centre-reported attendance count
3. Computed attendance discrepancy percentage
4. Configurable discrepancy threshold
5. Alert trigger & penalty assignment
"""
from typing import Dict, Any, Tuple

class AttendanceCrossCheckEngine:
    def __init__(self, moderate_threshold_pct: float = 15.0, critical_threshold_pct: float = 35.0):
        self.moderate_threshold_pct = moderate_threshold_pct
        self.critical_threshold_pct = critical_threshold_pct

    def cross_check(self, reported_count: int, estimated_count: int) -> Dict[str, Any]:
        """
        Computes discrepancy metric and alert classification.
        """
        if reported_count <= 0 and estimated_count <= 0:
            return {
                "reported_attendance": 0,
                "estimated_attendance": 0,
                "discrepancy_pct": 0.0,
                "alert_level": "NORMAL",
                "alert_triggered": False,
                "penalty_ratio": 0.0,
                "message": "Zero attendance recorded and verified."
            }

        base = max(reported_count, 1)
        discrepancy = abs(reported_count - estimated_count)
        discrepancy_pct = (discrepancy / base) * 100.0

        alert_level = "NORMAL"
        alert_triggered = False
        penalty_ratio = 0.0

        if discrepancy_pct > self.critical_threshold_pct:
            alert_level = "CRITICAL"
            alert_triggered = True
            penalty_ratio = min(1.0, discrepancy_pct / 100.0)
            msg = f"Critical attendance mismatch: Reported {reported_count} vs AI-Estimated {estimated_count} ({discrepancy_pct:.1f}% discrepancy)"
        elif discrepancy_pct > self.moderate_threshold_pct:
            alert_level = "MODERATE"
            alert_triggered = True
            penalty_ratio = discrepancy_pct / 100.0 * 0.6
            msg = f"Moderate attendance discrepancy: Reported {reported_count} vs AI-Estimated {estimated_count} ({discrepancy_pct:.1f}% discrepancy)"
        else:
            msg = f"Attendance verified within normal margin ({discrepancy_pct:.1f}% discrepancy)"

        return {
            "reported_attendance": reported_count,
            "estimated_attendance": estimated_count,
            "discrepancy_pct": round(discrepancy_pct, 2),
            "alert_level": alert_level,
            "alert_triggered": alert_triggered,
            "penalty_ratio": round(penalty_ratio, 3),
            "message": msg
        }
