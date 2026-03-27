from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from enum import Enum
from datetime import datetime
class status(str, Enum):
  pening = "Pending"
  approved = "Approved"
  rejected = "Rejected"
  
class request(BaseModel):
  id: UUID =  Field(default_factory=uuid4)
  emp_id: UUID
  cmp_id: UUID
  reason: str
  doc: str | None
  status: status
  date: datetime = Field(default_factory=datetime.utcnow)
  start_date: datetime
  end_date: datetime
