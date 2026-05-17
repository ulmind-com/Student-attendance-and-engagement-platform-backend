from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class Student(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    firstName: str
    lastInitial: str
    rollNumber: str
    class_name: Optional[str] = "Nursery-A"
    section: Optional[str] = "A"
    parentsName: Optional[str] = ""
    parentsPhone: Optional[str] = ""
    bloodGroup: Optional[str] = ""
    profilePhoto: Optional[str] = ""
    attendance: int = 100
    risk: str = "Stable"
    parentStatus: str = "Pending"
    timeline: List[dict] = []
    status: Optional[str] = "active"
    
    class Config:
        populate_by_name = True
        extra = "allow"


class Teacher(BaseModel):
    teacher_id: str
    name: str
    class_name: str

class EmotionalCheckin(BaseModel):
    roll_number: str
    feeling_level: int
    selected_emoji: str
    questions: Dict[str, bool]
    date: datetime = Field(default_factory=datetime.utcnow)

class Attendance(BaseModel):
    roll_number: str
    status: str # "Present", "Absent", "Late"
    date: datetime = Field(default_factory=datetime.utcnow)

class WellnessAlert(BaseModel):
    roll_number: str
    alert_level: str # "soft", "red_flag"
    message: str
    resolved: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
