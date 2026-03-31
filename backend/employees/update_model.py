from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber

class UpdateEmpByEmp(BaseModel):
    password: str | None = None
    phone: PhoneNumber | None = None
    emergency_phone: PhoneNumber | None = None

