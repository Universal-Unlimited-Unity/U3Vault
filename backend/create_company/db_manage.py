from sqlalchemy import Table, Column, String, MetaData, insert, DateTime, select
from sqlalchemy.dialects.postgresql import UUID
from .model import Company
from db.db_connect import db_connect
from datetime import datetime

eng = db_connect()
metadata = MetaData()

company_table = Table(
    "company",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("name", String, nallable=False)
    Column("email", String, nullable=False, unique=True),
    Column("password", String, nullable=False),
    Column("address", String | None, nullable=True),
    Column("phone_number", String | None, nullable=True),
    Column("slug", String, nullable=False, unique=True),
    Column("created_at", DateTime, default=datetime.utcnow),
)

def init():
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
                slug=company.slug,
                created_at=datetime.utcnow()
            )
        )
        conn.commit()
        return company.id

def check_slug(slug: str):
    with eng.connect() as conn:
        stmt = select(company).where(company.c.slug == slug)
        row = conn.execute(stmt).fetchone()
        return row
def generate_slug(name: str):
    slug = name.split()[0]
    count = 1
    while check_slug(slug):
        slug = slug + str(count)
        count += 1
    return slug
        
