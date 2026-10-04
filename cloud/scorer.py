"""
Satark AI - Session Integrity Score (SIS) Scorer (FR-9)
Calculates deterministic 0–100 composite compliance score per centre per session:
SIS = max(0, 100 - (WA * PA + WF * PF + WE * PE + WT * PT + WC * PC))
Ranks centres into Risk Tiers:
- High Risk (<50): Immediate Physical Audit Dispatch
- Moderate Risk (50-75): Enhanced Surveillance
- Compliant (>75): Verified
"""
from typing import Dict, Any, List

class SISScorer:
    def __init__(self,
                 weight_attendance: float = 30.0,
                 weight_feed_integrity: float = 25.0,
                 weight_equipment: float = 20.0,
                 weight_trainer: float = 15.0,
                 weight_collusion: float = 10.0):
        self.w_attendance = weight_attendance
        self.w_feed = weight_feed_integrity
        self.w_equipment = weight_equipment
        self.w_trainer = weight_trainer
        self.w_collusion = weight_collusion

    def compute_sis(self,
                    attendance_penalty_ratio: float,
                    feed_tamper_count: int,
                    equipment_statuses: List[Dict[str, Any]],
                    trainer_present: bool,
                    collusion_detected: bool) -> Dict[str, Any]:
        
        # 1. Attendance penalty (0 to 30)
        p_attendance = min(1.0, max(0.0, attendance_penalty_ratio)) * self.w_attendance

        # 2. Feed integrity penalty (0 to 25)
        p_feed = min(self.w_feed, feed_tamper_count * 25.0)

        # 3. Equipment compliance penalty (0 to 20)
        total_items = max(1, len(equipment_statuses))
        non_compliant_count = 0
        for eq in equipment_statuses:
            if eq.get("apparent_operability") in ["ABSENT", "IDLE"]:
                non_compliant_count += 1
        p_equipment = (non_compliant_count / total_items) * self.w_equipment

        # 4. Trainer presence penalty (0 to 15)
        p_trainer = 0.0 if trainer_present else self.w_trainer

        # 5. Collusion penalty (0 to 10)
        p_collusion = self.w_collusion if collusion_detected else 0.0

        total_penalty = p_attendance + p_feed + p_equipment + p_trainer + p_collusion
        sis_score = max(0.0, round(100.0 - total_penalty, 1))

        if sis_score < 50.0:
            risk_tier = "HIGH_RISK"
            audit_recommended = True
        elif sis_score < 75.0:
            risk_tier = "MODERATE_RISK"
            audit_recommended = False
        else:
            risk_tier = "COMPLIANT"
            audit_recommended = False

        flags = []
        if p_attendance > 10.0:
            flags.append("ATTENDANCE_MISMATCH")
        if p_feed > 0:
            flags.append("FEED_TAMPER_SUSPECTED")
        if p_equipment > 5.0:
            flags.append("EQUIPMENT_UNDERUTILIZED_OR_ABSENT")
        if not trainer_present:
            flags.append("TRAINER_ABSENCE")
        if collusion_detected:
            flags.append("MULTI_CENTRE_COLLUSION")

        return {
            "sis_score": sis_score,
            "risk_tier": risk_tier,
            "audit_recommended": audit_recommended,
            "flags": flags,
            "penalties": {
                "attendance": round(p_attendance, 1),
                "feed_integrity": round(p_feed, 1),
                "equipment": round(p_equipment, 1),
                "trainer": round(p_trainer, 1),
                "collusion": round(p_collusion, 1)
            }
        }
