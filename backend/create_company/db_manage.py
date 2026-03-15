from sqlalchemy import Table, Column, String, MetaData, insert
from sqlalchemy.dialects.postgresql import UUID
from .model import Company
from db.db_connect import db_connect

eng = db_connect()
metadata = MetaData()

company_table = Table(
    "company",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("email", String, nullable=False, unique=True),
    Column("password", String, nullable=False),
    Column("address", String, nullable=True),
    Column("phone_number", String, nullable=True),
)

def init()
    metadata.create_all(eng, checkfirst=True)
    
def insert_company(company: Company):
    
    with eng.connect() as conn:
        conn.execute(
            company_table.insert().values(
                id=company.id,
                email=company.email,
                password=company.password,
                address=company.address,
                phone_number=company.phone_number,
            )
        )
        conn.commit()
        return company.id
    