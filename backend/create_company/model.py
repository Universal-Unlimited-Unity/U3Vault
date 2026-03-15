from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from typing import Optional

class Company(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    password: str
    address: str | None
    phone_number: str | None
    