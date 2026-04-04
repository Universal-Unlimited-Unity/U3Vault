from fastapi import APIRouter, HTTPException, Body, Header, Query
from .model import request
from .db_manage import get_req_by_status, add_req, update_req
from shared.func import lazy 
from typing import Annotated
import uuid
router = APIRouter(prefix="/requests", tags=["requests"])

@router.post("")
async def insert_res(request_: Annotated[request, Body()], auth: Annotated[str, Header()]):
  user = lazy(auth)
  if user["role"] == "Employee":
    add_req(request_)
  else:
    raise HTTPException(status_code=401)

@router.get("")
async def get_req(status : Annotated[str, Query()], auth: Annotated[str, Header()]):
  user = lazy(auth)
  if user["role"] == "Employee":
    return get_req_by_status(status, user["id"])

@router.get("/AdMan")
async def get_req(auth: Annotated[str, Header()]):
    user = lazy(auth)
    if user["role"] == "Employee":
      raise HTTPException(status_code = 401)
    else:
      return get_req_for_manager_by_status(uuid.UUID(user["company_id"]))
@router.patch("/AdMan")
async def update_req(id: Annotated[uuid.UUID, Query()], status: Annotated[str, Query()], auth: Annotated[str, Header()]):
  user = lazy()
  if user["role"] == "Employee":
    raise HTTPException(status_code = 401)
  else:    
    update_req(id, status)
