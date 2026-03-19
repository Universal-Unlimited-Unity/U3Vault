from sqlalchemy import select
from passlib_context import CryptContext
from db.db_connect import db_connect
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()
pwd_context = CryptContext(shemes=["bcrypt"], deprecated="auto")
eng = db_connect()

TOKEN_EXP_MIN = os.getenv("TOKEN_EXP_MIN")
TOKEN_KEY = os.getenv("TOKEN_KEY")
ALGO = os.getenv("ALGO")

def admin_auth(email: str, pwd: str):
  with eng.connect() as conn:
    stmt = select(company).where(company.c.email == email)
    company = conn.execute(stmt).fetchone()
    if not company:
      return None
    if not pwd_context.verify(password, company.password):
      return None
    payload = {
      "role": "admin",
      "company_id": str(company.id),
      "exp": datetime.utcnow() + timedelta(minutes=int(TOKEN_EXP_MIN))
      }
    return jwt.encode(payload, TOKEN_KEY, algorithme=ALGO)

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
    if not pwd_context.verify(password, user.password):
      return None
    payload = {
      "id": str(user.id),
      "role": user.role,
      "company_id": str(user.company_id),
      "exp": datetime.utcnow() + timedelta(minutes:int(TOKEN_EXP_MIN))
      }
    return jwt.encode(payload, TOKEN_KEY, algorithme=ALGO)
