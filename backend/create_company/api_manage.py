from fastapi import APIRouter, HTTPException
from .db_manage import insert_company, check_slug, generate_slug
from .model import Company
from passlib_context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/company", tags=["company"])
@router.post("/")
async def create_company_api(company: Company):
    company.slug = generate_slug(company.name)
    company.password = pwd_context.hash(company.password)    
    company_id = insert_company(company)
    if not company_id:
        raise HTTPException(status_code=500, detail="Failed to create company")
    return str(company_id)
