from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
db = "postgresql+psycopg://postgres:adamaakif@db:5432/vault"
def db_connect():
    eng = create_engine(db)
    return eng


