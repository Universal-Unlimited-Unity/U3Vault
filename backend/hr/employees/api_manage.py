from fastapi import FastAPI, HTTPException, Path, Query
from contextlib import asynccontextmanager
from .db_manage import init, add, listall_selectbox, delete_emp, listall, select_emp
from .model import Employee
from typing import Annotated
asynccontextmanager
async def lifespan(app: FastAPI):
    init()
    print("Employee Table Created!")
    yield
    print("Shutting Down...")    
    
app = FastAPI(lifespan=lifespan)

@app.post("/employees", response_model=Employee)
async def add_api(emp: Employee) -> Employee:
    return add(emp)

@app.get("/employees")
async def listall_selectbox_api():
    result = listall_selectbox()
    if result == 1:
        raise HTTPException(status_code=404)
    return result

@app.get("/employees/dataframe", response_model=list[Employee])
async def listall_api():
    result = listall()
    if not result:
        raise HTTPException(statuts_code=404)
    else:
        return result

@app.get("/employees/{id}", response_model=Employee)
async def select_emp_api(id: Annotated[str, Path()]):
    return select_emp(id)
    
@app.delete("/employees/{id}", response_model=Employee)
async def delete_emp_api(id: Annotated[str, Path()]):
    return delete_emp(id)
