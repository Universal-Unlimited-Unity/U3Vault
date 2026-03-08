from sqlalchemy import MetaData, Table, Column
from db.db_connect import db_connect
eng = db_connect()

metadata = MetaData()
Attendance = Table(
    "Attendance",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True)
)