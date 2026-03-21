from fastapi import APIRouter, HTTPException, Path
from .db_manage import insert_company, check_slug, generate_slug
from .model import Company
from passlib.context import CryptContext
from typing import Annotated

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/company", tags=["company"])
@router.post("/")
async def create_company_api(company: Company):
    company.password = pwd_context.hash(company.password)    
    company_id = insert_company(company)
    if not company_id:
        raise HTTPException(status_code=500, detail="Failed to create company")
    return str(company_id)

@router.get("/{name}")
async def gen_slug(name: Annotated[str, Path()]):
    slug = generate_slug(name)
    return slug
