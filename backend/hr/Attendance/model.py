from pydantic import BaseModel
from enum import Enum
import uuid
from datetime import date
class Status(str, Enum):
    Present = "Present"
    Absent = "Absent"
    Sick = "Sick"
    Vacation = "Vacation"
    Remote = "Remote"

class Attendance(BaseModel):
    id: uuid.UUID
    first_name: str
    middle_name: str
    last_name: str
    date: date
    status: Status
