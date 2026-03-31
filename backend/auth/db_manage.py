from sqlalchemy import select
from passlib.context import CryptContext
from db.db_connect import db_connect
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os
from employees.db_manage import employees
from create_company.db_manage import company
from uuid import UUID
load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
eng = db_connect()

TOKEN_EXP_MIN = os.getenv("TOKEN_EXP_MIN")
TOKEN_KEY = os.getenv("TOKEN_KEY")
ALGO = os.getenv("ALGO")

def admin_auth(email: str, pwd: str):
  with eng.connect() as conn:
    stmt = select(company).where(company.c.email == email)
    company_ = conn.execute(stmt).fetchone()
    if not company_:
      return None
    if not pwd_context.verify(pwd, company_.password):
      return None
    payload = {
      "role": "Admin",
      "company_id": str(company_.id),
      "exp": datetime.utcnow() + timedelta(minutes=int(TOKEN_EXP_MIN))
      }
    return jwt.encode(payload, TOKEN_KEY, algorithm=ALGO)

def reg_auth(slug: str, email: str, pwd: str):
  with eng.connect() as conn:
    stmt = select(company.c.id).where(company.c.slug == slug)
    comp_id = conn.execute(stmt).fetchone()
    if not comp_id:
      return None
    stmt = select(employees).where(employees.c.company_id == comp_id.id, employees.c.email == email)
    user = conn.execute(stmt).fetchone()
    if not user:
      return None
    if not pwd_context.verify(pwd, user.password):
      return None
    payload = {
      "id": str(user.id),
      "role": user.role,
      "company_id": str(user.company_id),
      "exp": datetime.utcnow() + timedelta(minutes=int(TOKEN_EXP_MIN))
      }
    return jwt.encode(payload, TOKEN_KEY, algorithm=ALGO)

def verify_pwd(id: UUID, pwd: str):
  with eng.connect() as conn:
    secret = conn.execute(select(employees.c.password).where(employees.c.id == id)).first()
    return pwd_context.verify(pwd, secret.password)
    
    
