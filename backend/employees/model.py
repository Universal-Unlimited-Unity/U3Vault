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

class role(str, Enum):
    manager = "Manager"
    employee = "Employee"

class Employee_s(BaseModel):
    first_name: str
    last_name: str
    role: role
    phone: PhoneNumber
    email: EmailStr
    department: str
    contract_pdf
    status: status
    department: str

class Employee_for_listall(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    job_name: str | None
    first_name: str
    last_name: str
    middle_name: str | None
    role: role
    supervisor: str | None
    gender: gender
    dob: date
    phone: PhoneNumber
    email: EmailStr
    address: str
    department: str
    start_date: date
    emergency_phone: PhoneNumber | None
    employment_type: employment_type
    contract_type: contract_type 
    status: status

class Employee(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    job_name: str | None
    company_id: UUID
    first_name: str
    last_name: str
    middle_name: str | None
    role: role
    supervisor: str | None
    gender: gender
    dob: date
    phone: PhoneNumber
    email: EmailStr
    password: str
    address: str
    photo: str | None
    department: str
    start_date: date
    contract_pdf: str | None
    emergency_phone: PhoneNumber | None
    employment_type: employment_type
    contract_type: contract_type 
    status: status
