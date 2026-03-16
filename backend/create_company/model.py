from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from datetime import datetime

class Company(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    password: str
    address: str | None
    phone_number: str | None
    slug: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
