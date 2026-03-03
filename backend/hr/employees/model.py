from pydantic import BaseModel, EmailStr, Field
from datetime import date
from enum import Enum
from pydantic_extra_types.phone_numbers import PhoneNumber
from uuid import UUID, uuid4
class gender(str, Enum):
    Male = "Male"
    Female = "Female"
    
class status(str, Enum):
    Active = "Active"
    On_Leave = "On Leave"
    Inactive = "Inactive"
    Resigned = "Resigned"
    
class contract_type(str, Enum):
    Employee = "Employee"
    Temporary = "Temporary"
    Intern = "Intern"

class employment_type(str, Enum):
    Full_time = "Full-time"
    Part_time = "Part-time"


class Employee(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    middle_name: str | None
    role: str
    supervisor: str | None
    gender: gender
    dob: date
    phone: PhoneNumber
    email: EmailStr
    adress: str
    photo: str
    department: str
    start_date: date
    contract_pdf: str
    emergency_phone: PhoneNumber
    employment_type: employment_type
    contract_type: contract_type
    status: status

    
    

