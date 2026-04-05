from db.db_connect import db_connect, metadata
from .model import request as request_model
from sqlalchemy import insert, Table, Column, String, Date, select, delete, ForeignKey, UniqueConstraint, DateTime, update
import uuid
from sqlalchemy.dialects.postgresql import UUID
from create_company.db_manage import company
from employees.db_manage import employees

eng = db_connect()

request = Table(
  "request",
  metadata,
  Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
  Column("emp_id", UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False),
  Column("cmp_id", UUID(as_uuid=True), ForeignKey("company.id", ondelete="CASCADE"), nullable=False),
  Column("reason", String, nullable=False),
  Column("doc", String, nullable=True),
  Column("status", String, nullable=False),
  Column("date", DateTime, nullable=False),
  Column("start_date",DateTime, nullable=False),
  Column("end_date", DateTime, nullable=False)
)

def init():
  metadata.create_all(eng, checkfirst=True)

def add_req(request_: request_model):
  with eng.connect() as conn:
    stmt = insert(request).values(request_.model_dump())
    conn.execute(stmt)
    conn.commit()

def get_req_by_status(status: str, id: uuid.UUID):
  with eng.connect() as conn:
    if status.title() != "All":
      stmt = select(request.c.date, request.c.reason, request.c.status).where(request.c.status == status, request.c.emp_id == id)
    else:
      stmt = select(request.c.date, request.c.reason, request.c.status).where(request.c.emp_id == id)
      
    reqs = conn.execute(stmt).mappings().fetchall()
    return reqs

def get_req_for_manager_by_status(cmp_id: uuid.UUID):
  with eng.connect() as conn:
    stmt = select(request.c.id, request.c.reason, request.c.doc, 
                  request.c.date, request.c.start_date, request.c.end_date, 
                  request.c.emp_id, employees.c.first_name, employees.c.last_name).join(employees).where(request.c.status == "Pending", request.c.cmp_id == cmp_id)
    rows = conn.execute(stmt).mappings().fetchall()
    return rows

def update_req(id: uuid.UUID, status_: str):
  with eng.connect() as conn:
    stmt = update(request).where(request.c.id == id).values(status = status_)
    conn.execute(stmt)
    conn.commit()
