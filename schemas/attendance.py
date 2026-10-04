from pydantic import BaseModel
from typing import Optional

class AttendanceRecord(BaseModel):
    centre_id: str
    batch_session_id: str
    date: str
    scheduled_start: str
    scheduled_end: str
    reported_attendance_count: int
    course_name: Optional[str] = "General Skilling"
    trainer_name: Optional[str] = "Sanctioned Instructor"
