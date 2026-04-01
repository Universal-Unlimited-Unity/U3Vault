from fastapi import APIRouter, HTTPException, Path, Header
from .db_manage import insert_company, check_slug, generate_slug, cmp_name
from .model import Company
from passlib.context import CryptContext
from typing import Annotated
from shared.func import lazy, check_pwd
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/company", tags=["company"])
@router.post("")
async def create_company_api(company: Company):
    if not check_pwd(company.password):
        raise HTTPException(status_code = 404)
    company.password = pwd_context.hash(company.password)    
    company_id = insert_company(company)
    if not company_id:
        raise HTTPException(status_code=500, detail="Failed to create company")
    return str(company_id)

@router.get("/{name}")
async def gen_slug(name: Annotated[str, Path()]):
    slug = generate_slug(name)
    return slug

@router.get("")
async def get_cmp_name(auth: Annotated[str, Header()]):
    user = lazy(auth)
    return cmp_name(user["company_id"])