from pydantic import BaseModel
from typing import Dict, Any, Optional

class AlertBlock(BaseModel):
    block_index: int
    timestamp: str
    centre_id: str
    session_id: str
    alert_type: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    description: str
    details: Dict[str, Any]
    previous_hash: str
    block_hash: str
