from pydantic import BaseModel
from typing import Dict, List, Optional

class PenaltyBreakdown(BaseModel):
    attendance_penalty: float = 0.0
    feed_integrity_penalty: float = 0.0
    equipment_penalty: float = 0.0
    trainer_penalty: float = 0.0
    collusion_penalty: float = 0.0

class SISRecord(BaseModel):
    centre_id: str
    session_id: str
    timestamp: str
    sis_score: float
    risk_level: str  # HIGH_RISK (<50), MODERATE_RISK (50-75), COMPLIANT (>75)
    penalties: PenaltyBreakdown
    flags: List[str]
    audit_recommended: bool
