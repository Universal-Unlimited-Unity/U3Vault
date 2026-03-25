from fastapi import APIRouter, HTTPException
from .model import request
from .db_manage import def get_req_by_status
from shared.func import lazy 
router = APIRouter(prefix="/requests", tags=["/requests"])

router.post("/")
async def insert_res(request_:request, auth: str):
  user = lazy(auth)
  if user["role"] == "Employee":
    get_req_by_status(request_)
  else:
    raise HTTPException(status_code=401)
    
  
