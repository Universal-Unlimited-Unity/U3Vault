from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from enum import Enum

class status(str, Enum):
  pening = "Pending"
  approved = "Approved"
  rejected = "Rejected"
  
class request(BaseModel):
  req_id: UUID =  Field(default_factory=uuid4)
  emp_id: UUID
  reason: str
  doc: str | None
  status: status
