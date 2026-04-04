from fastapi import APIRouter, HTTPException, Path, Header, Query
from .db_manage import insert_company, check_slug, generate_slug, cmp_name, get_slug, update_pwd
from .model import Company
from passlib.context import CryptContext
from typing import Annotated
from shared.func import lazy, check_pwd
import uuid
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
    return cmp_name(uuid.UUID(user["company_id"]))
    
@router.get("/slug")
async def get_cmp_slug(auth: Annotated[str, Header()]) -> str:
    user = lazy()
    return get_slug(uuid.UUID(user["company_id"]))

@router.patch("")
async def update_pwd_api(password: Annotated[str, Query()], auth: Annotated[str, Header()]):
    user = lazy()
    update_pwd(uuid.UUID(user["company_id"]), password)


