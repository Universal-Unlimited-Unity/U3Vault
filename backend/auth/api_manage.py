from fastapi import APIRouter, HTTPException, Path, Body, Header, Query
from typing import Annotated
from .db_manage import admin_auth, reg_auth, verify_pwd, verify_pwd_admin
from .model import admin, regular
from uuid import UUID
from shared.func import lazy
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def auth(login: Annotated[admin | regular, Body()]):
  if login.role == "Admin":
    token = admin_auth(login.email, login.password)
    if not token:
      raise HTTPException(status_code=401, detail="Wrong Infos")
    return {"token": token}
  else:
    token = reg_auth(login.slug, login.email, login.password)
    if not token:
      raise HTTPException(status_code=401, detail="Wrong Infos")
    return {"token": token}
      
@router.post("/verify")
async def verify_pwd_api(pwd: Annotated[str, Query()], auth: Annotated[str, Header()]):
  user = lazy(auth)
  id = UUID(user["id"])
  if not verify_pwd(id, pwd):
    raise HTTPException(status_code = 401)
  
@router.post("/verify/token")
async def check_token(auth: Annotated[str, header()]):
  try:
    lazy(auth)
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code = 401)

@router.post("/verify/admin)
async def check_pwd_api(pwd: Annotated[str, Query()], auth: Annotated[str, Header()]):
  user = lazy(auth)
  if not verify_pwd_admin(UUID(user["company_id"]), pwd):
    raise HTTPException(status_code = 401)
