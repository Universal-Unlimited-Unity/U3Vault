from fastapi import APIRouter, HTTPException, Path, Header, Body
from .db_manage import add, listall_selectbox, delete_emp, listall, select_emp, update_emp_by_emp, get_contract
from .model import Employee, Employee_s, Employee_for_listall
from typing import Annotated
from jose import jwt
from dotenv import load_dotenv
import os
from passlib.context import CryptContext
from shared.func import lazy
from .update_model import UpdateEmpByEmp
from uuid import UUID
from shared.func import check_pwd
from sqlalchemy.exc import IntegrityError
router = APIRouter(prefix="/employees", tags=["employees"])

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")   
@router.post("")
async def add_api(emp: Annotated[Employee, Body()], auth: Annotated[str, Header()]) -> Employee:
    user = lazy(auth)
    if user["role"] == "Admin" or user["role"] == "Manager":
        emp.password = pwd_context.hash(emp.password)
        try:
            add(emp)
            raise HTTPException(status_code=200)
        except IntegrityError as e:
            raise HTTPException(status_code=409)
        
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

@router.patch("")
async def update_by_emp(auth: Annotated[str, Header()], update: Annotated[UpdateEmpByEmp, Body()]):
    user = lazy(auth)
    if update.password:
        if not check_pwd(update.password):
            raise HTTPException(status_code=404)
    id = UUID(user["id"])
    update_emp_by_emp(id, update)
    
@router.get("/dataframe", response_model=list[Employee_for_listall])
async def listall_api(auth: Annotated[str, Header()]):
    user = lazy(auth)
    if user["role"] == "Employee":
        raise HTTPException(status_code==401)
    result = listall()
    if not result:
        raise HTTPException(status_code=404)
    else:
        return result

@router.get("/{id}", response_model=Employee_s)
async def select_emp_api(id: Annotated[str, Path()], auth: Annotated[str, Header()]):
    user = lazy(auth)
    return select_emp(id)
    
@router.delete("/{id}", response_model=Employee_for_listall)
async def delete_emp_api(id: Annotated[str, Path()], auth: Annotated[str, Header()]):
    user = lazy(auth)
    if not user["role"] == "Admin":
        raise HTTPException(status_code=401)
    return delete_emp(id)

@router.get("/contracts/{id}")
async def get_contract_api(id: Annotated[UUID, Path()], auth: Annotated[str, Header()]):
    lazy(auth)
    contract = get_contract(id)
    if contract:
        return contract
    raise HTTPException(status_code = 404)

