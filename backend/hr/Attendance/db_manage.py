from sqlalchemy import MetaData, Table, Column, ForeignKey, String, Date, select, insert
from db.db_connect import db_connect

eng = db_connect()

metadata = MetaData()
Attendance = Table(
    "Attendance",
    metadata,
    Column("id", UUID(as_uuid=True), ForeignKey("employees.id", ondelete="SET NULL"),
           nullable=True),
    Column("first_name", String, nullable=False),
    Column("middle_name", String, nullable=True),
    Column("last_name", String, nullable=False),
    Column("date", Date, nullable=False)
    Column("status", String, nullable=False)
)

def init() -> None:
    metadata.create_all(eng, ckeckfirst=True)

def emp_attendance_dict():
    with eng.connect() as conn:
        emps = select(employees).mappings().all()
        if not emps:
            return 1
        newhash = {}
        for i in emps:
            middle_name = i["middle_name"] if emp["middle_name"] else ""
            newhash[str(i["id"])] = {"id": i["id"], "first_name": i["first_name"], "middle_name": middle_name, "last_name": i["last_name"], "status":""}
        return newhash
        
def insert(att: list[dict[str, str]]):
    with eng.connect() as conn:
        conn.execute(insert(attendance), att)
        conn.commit()
    
    
                                     
