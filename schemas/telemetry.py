"""
Satark AI - Pydantic Schemas for Vigilance & Telemetry
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal
from datetime import datetime

class EquipmentItemStatus(BaseModel):
    item: str
    sanctioned_count: int
    detected_count: int
    present: bool
    apparent_operability: Literal["USED", "IDLE", "ABSENT"]
    interaction_minutes: float = 0.0

class FeedHealth(BaseModel):
    status: Literal["OK", "BLACKOUT", "FROZEN", "MOVED", "COVERED", "OFFLINE"]
    confidence: float = 1.0
    last_frame_timestamp: str

class DwellCurveSummary(BaseModel):
    window_minutes: int = 5
    timestamps: List[str]
    headcounts: List[int]
    sustained_headcount: int
    peak_headcount: int
    collapse_detected: bool = False
    collapse_ratio: float = 0.0

class TelemetryPayload(BaseModel):
    centre_id: str
    timestamp: str
    session_id: str
    estimated_attendance: int
    reported_attendance: Optional[int] = None
    attendance_discrepancy: float = 0.0
    attendance_alert: bool = False
    dwell_curve_summary: DwellCurveSummary
    equipment_status: List[EquipmentItemStatus]
    feed_health: FeedHealth
    trainer_present: bool = True
    sis_score: float = 100.0
    prev_hash: str
    signature: str = ""
