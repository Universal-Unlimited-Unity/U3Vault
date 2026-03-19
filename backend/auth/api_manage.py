from fastapi import APIRouter, HTTPException
from .db_manage import admin_auth, reg_auth
from .model import admin, regular

router = APIRouter(prefix="/auth", tags=["auth"])

router.post("/login")
async def auth(login: admin | regular):
  if login.role == "Admin":
    token = admin_auth(login.email, login.password)
    if not token:
      raise HTTPException(status_code=401, detail="Wrong Infos")
    return {"token": token}
  else:
    token = admin_auth(login.slug, login.email, login.password)
    if not token:
      raise HTTPException(status_code=401, detail="Wrong Infos")
    return {"token": token}
      
