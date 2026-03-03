from sqlalchemy import create_engine

db = "postgresql+psycopg://postgres:adamaakif@db:5432/vault"

def db_connect():
    eng = create_engine(db)
    return eng


