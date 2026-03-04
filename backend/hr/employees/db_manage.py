from db.db_connect import db_connect
from .model import Employee
from sqlalchemy import insert, Table, Column, MetaData, String, Date
import uuid
from sqlalchemy.dialects.postgresql import UUID

eng = db_connect()
metadata = MetaData()

employees = Table(
    "employees",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("middle_name", String, nullable=True),
    Column("role", String, nullable=False),
    Column("supervisor", String, nullable=True),
    Column("gender", String, nullable=False),
    Column("dob", Date, nullable=False),
    Column("phone", String, nullable=False),
    Column("email", String, nullable=False, unique=True),
    Column("address", String, nullable=False),
    Column("photo", String, nullable=True),
    Column("department", String, nullable=False),
    Column("start_date", Date, nullable=False),
    Column("contract_pdf", String, nullable=True),
    Column("emergency_phone", String, nullable=False),
    Column("employment_type", String, nullable=False),
    Column("contract_type", String, nullable=False),
    Column("status", String, nullable=False),
) 

def init():
    metadata.create_all(eng, checkfirst=True)

def add(emp: Employee) -> Employee:
    
    with eng.connect() as conn:
        stmt = insert(employees).values(
            id=emp.id,
            first_name=emp.first_name,
            last_name=emp.last_name,
            middle_name=emp.middle_name,
            role=emp.role,
            supervisor=emp.supervisor,
            gender=emp.gender.value,
            dob=emp.dob,
            phone=emp.phone,
            email=emp.email,
            address=emp.adress,
            photo=emp.photo,
            department=emp.department,
            start_date=emp.start_date,
            contract_pdf=emp.contract_pdf,
            emergency_phone=emp.emergency_phone,
            employment_type=emp.employment_type.value,
            contract_type=emp.contract_type.value,
            status=emp.status.value,
            )  
        conn.execute(stmt)
        conn.commit()
        return emp