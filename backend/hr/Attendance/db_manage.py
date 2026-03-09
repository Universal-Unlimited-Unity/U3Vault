from sqlalchemy import MetaData, Table, Column, ForeignKey, String, Date, select, insert
from db.db_connect import db_connect
from datetime import date
from sqlalchemy.dialects.postgresql import UUID
from hr.employees.db_manage import employees
eng = db_connect()

metadata = MetaData()
attendance = Table(
    "attendance",
    metadata,
    Column("id", UUID(as_uuid=True), nullable=True),
    Column("first_name", String, nullable=False),
    Column("middle_name", String, nullable=True),
    Column("last_name", String, nullable=False),
    Column("date", Date, nullable=False),
    Column("status", String, nullable=False)
)

def init() -> None:
    metadata.create_all(eng, checkfirst=True)

def emp_attendance_dict():
    with eng.connect() as conn:
        emps = select(employees).mappings().fetchall()
        if not emps:
            return 1
        newhash = {}
        for i in emps:
            middle_name = i["middle_name"] if i["middle_name"] else ""
            newhash[str(i["id"])] = {"id": str(i["id"]), "first_name": i["first_name"], "middle_name": middle_name, "last_name": i["last_name"], "status":""}
        return newhash
        
def insert(att: list[dict[str, str]]):
    with eng.connect() as conn:
        conn.execute(insert(attendance), att)
        conn.commit()

def check_date(att_date: date):
    with eng.connect() as conn:
        stmt = select(attendance).where(attendance.c.date == att_date)
        res = conn.execute(stmt).fetchone()
        return res
                                     
