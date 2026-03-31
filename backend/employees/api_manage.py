from fastapi import APIRouter, HTTPException, Path, Header, Body
from .db_manage import add, listall_selectbox, delete_emp, listall, select_emp, update_emp_by_emp
from .model import Employee
from typing import Annotated
from jose import jwt
from dotenv import load_dotenv
import os
from passlib.context import CryptContext
from shared.func import lazy
from .update_model import UpdateModelByEmp
from uuid import UUID
router = APIRouter(prefix="/employees", tags=["employees"])

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")   
@router.post("", response_model=Employee)
async def add_api(emp: Annotated[Employee, Body()], auth: Annotated[str, Header()]) -> Employee:
    user = lazy(auth)
    if user["role"] == "Admin":
        emp.password = pwd_context.hash(emp.password)
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
async def select_emp_api(id: Annotated[str, Path()], auth: Annotated[str, Header()]):
    user = lazy(auth)
    return select_emp(id)
    
@router.delete("/{id}", response_model=Employee)
async def delete_emp_api(id: Annotated[str, Path()], auth: Annotated[str, Header()]):
    user = lazy(auth)
    if not user["role"] == "Admin":
        raise HTTPException(status_code=401)
    return delete_emp(id)


@router.patch("")
async def update_by_emp(auth: Annotated[str, Header()], update: Annotated[UpdateModelByEmp, Body()]):
    user = lazy(auth)
    id = UUID(user["id"])
    update_emp_by_emp(id, update)
