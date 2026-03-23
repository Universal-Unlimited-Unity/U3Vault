from sqlalchemy import Table, Column, String, MetaData, insert, DateTime, select
from sqlalchemy.dialects.postgresql import UUID
from .model import Company
from db.db_connect import db_connect, metadata
from datetime import datetime

eng = db_connect()

company = Table(
    "company",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("name", String, nullable=False),
    Column("email", String, nullable=False, unique=True),
    Column("password", String, nullable=False),
    Column("address", String, nullable=True),
    Column("phone_number", String, nullable=True),
    Column("slug", String, nullable=False, unique=True),
    Column("created_at", DateTime, default=datetime.utcnow),
)

def init():
    metadata.create_all(eng, checkfirst=True)

def insert_company(company_: Company):
    with eng.connect() as conn:
        conn.execute(
            insert(company).values(
                name=company_.name,
                id=company_.id,
                email=company_.email,
                password=company_.password,
                address=company_.address,
                phone_number=company_.phone_number,
                slug=company_.slug,
                created_at=company_.created_at
            )
        )
        conn.commit()
        return company_.id

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
        
def cmp_name(id: str):
    with eng.connect() as conn:
        stmt = select(company.c.name).where(company.c.id == id)
        row = conn.execute(stmt).fetchone()
        return row.name