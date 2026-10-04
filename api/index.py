import os
import sys

# Add root directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cloud.app import app, sis_rankings, ledger, audit_dispatch_queue

# Seed default active training centre state for live cloud demo
if not sis_rankings:
    sis_rankings["TC-DEL-0101"] = {
        "centre_id": "TC-DEL-0101",
        "last_session_id": "BATCH-DEL-2026-A1",
        "timestamp": "2026-10-04T09:30:00Z",
        "sis_score": 94.5,
        "risk_tier": "COMPLIANT",
        "audit_recommended": False,
        "penalties": {"attendance": 1.5, "feed_integrity": 0.0, "equipment": 4.0, "trainer": 0.0, "collusion": 0.0},
        "flags": [],
        "estimated_attendance": 19,
        "reported_attendance": 20,
        "discrepancy_pct": 5.0,
        "feed_health": "OK",
        "trainer_present": True
    }
    sis_rankings["TC-HAR-0204"] = {
        "centre_id": "TC-HAR-0204",
        "last_session_id": "BATCH-HAR-2026-B1",
        "timestamp": "2026-10-04T09:30:00Z",
        "sis_score": 42.0,
        "risk_tier": "HIGH_RISK",
        "audit_recommended": True,
        "penalties": {"attendance": 25.7, "feed_integrity": 0.0, "equipment": 10.0, "trainer": 0.0, "collusion": 0.0},
        "flags": ["ATTENDANCE_MISMATCH", "EQUIPMENT_UNDERUTILIZED_OR_ABSENT"],
        "estimated_attendance": 4,
        "reported_attendance": 28,
        "discrepancy_pct": 85.7,
        "feed_health": "OK",
        "trainer_present": True
    }
    sis_rankings["TC-UP-0309"] = {
        "centre_id": "TC-UP-0309",
        "last_session_id": "BATCH-UP-2026-C1",
        "timestamp": "2026-10-04T09:30:00Z",
        "sis_score": 68.0,
        "risk_tier": "MODERATE_RISK",
        "audit_recommended": False,
        "penalties": {"attendance": 8.0, "feed_integrity": 0.0, "equipment": 0.0, "trainer": 15.0, "collusion": 0.0},
        "flags": ["TRAINER_ABSENCE"],
        "estimated_attendance": 11,
        "reported_attendance": 15,
        "discrepancy_pct": 26.6,
        "feed_health": "OK",
        "trainer_present": False
    }

    ledger.append_alert(
        centre_id="TC-HAR-0204",
        session_id="BATCH-HAR-2026-B1",
        alert_type="ATTENDANCE_DISCREPANCY_CRITICAL",
        severity="CRITICAL",
        description="Punch-and-Leave detected: 28 reported vs 4 sustained presence (85.7% delta)",
        details={"discrepancy_pct": 85.7}
    )
    ledger.append_alert(
        centre_id="TC-UP-0309",
        session_id="BATCH-UP-2026-C1",
        alert_type="TRAINER_ABSENCE_ALERT",
        severity="MEDIUM",
        description="Trainer absent from podium zone during scheduled session",
        details={"trainer_present": False}
    )

    audit_dispatch_queue.append({
        "centre_id": "TC-HAR-0204",
        "session_id": "BATCH-HAR-2026-B1",
        "score": 42.0,
        "reason": "Low SIS score / Critical punch-and-leave fraud",
        "dispatched": False,
        "created_at": "2026-10-04T09:35:00Z"
    })
