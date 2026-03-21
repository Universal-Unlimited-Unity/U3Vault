from fastapi import APIRouter, HTTPException, Path, Header
from .db_manage import add, listall_selectbox, delete_emp, listall, select_emp
from .model import Employee
from typing import Annotated
from jose import jwt
from dotenv import load_env
import os
router = APIRouter(prefix="/employees", tags=["employees"])
load_env()
TOKEN_KEY = os.getenv("TOKEN_KEY")
ALGO = os.getnenv("ALGO")

def lazy(auth):
    token = auth.split()[1]
    user = jwt.decode(token, TOEKN_KEY, ALGO)
    return user
    
@router.post("", response_model=Employee)
async def add_api(emp: Employee, auth: Annotated[str, Header()]) -> Employee:
    user = lazy(auth)
    if user["role"] == "Admin":
        return add(emp)
    else:
        raise HTTPException(status_code=401)

@router.get("")
async def listall_selectbox_api(auth: Annotated[str, Header()]):
    user = lazy(auth)
    if user["role"] == "Employee":
        raise HTTPException(status_code=401)
    result = listall_selectbox()
    if result == 1:
        raise HTTPException(status_code=404)
    return result

@router.get("/dataframe", response_model=list[Employee])
async def listall_api(auth: Annotated[str, Header()]):
    user = lazy(auth)
    if user["role"] == "Employee":
        raise HTTPException(status_code==401)
    result = listall()
    if not result:
        raise HTTPException(status_code=404)
    else:
        return result

@router.get("/{id}", response_model=Employee)
async def select_emp_api(id: Annotated[str, Path()]):
    return select_emp(id)
    
@router.delete("/{id}", response_model=Employee, auth: Annotated[str, Header()]):
async def delete_emp_api(id: Annotated[str, Path()]):
    user = lazy(auth)
    if not user["role"] == "Admin":
        raise HTTPException(status_code=401)
    return delete_emp(id)
