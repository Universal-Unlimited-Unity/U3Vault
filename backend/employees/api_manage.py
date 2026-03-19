from fastapi import APIRouter, HTTPException, Path
from .db_manage import add, listall_selectbox, delete_emp, listall, select_emp
from .model import Employee
from typing import Annotated

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("", response_model=Employee)
async def add_api(emp: Employee) -> Employee:
    return add(emp)

@router.get("")
async def listall_selectbox_api():
    result = listall_selectbox()
    if result == 1:
        raise HTTPException(status_code=404)
    return result

@router.get("/dataframe", response_model=list[Employee])
async def listall_api():
    result = listall()
    if not result:
        raise HTTPException(status_code=404)
    else:
        return result

@router.get("/{id}", response_model=Employee)
async def select_emp_api(id: Annotated[str, Path()]):
    return select_emp(id)
    
@router.delete("/{id}", response_model=Employee)
async def delete_emp_api(id: Annotated[str, Path()]):
    return delete_emp(id)
