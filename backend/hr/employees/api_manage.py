from fastapi import FastAPI, HTTPException, Path
from contextlib import asynccontextmanager
from .db_manage import init, add, listall, delete_emp
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
async def listall_api():
    result = listall()
    if result == 1:
        raise HTTPException(status_code=404)
    return result

@app.delete("/employees/{id}", response_model=Employee)
async def delete_emp_api(id: Annotated[str, Path()]):
    emp = delete_emp(id)
    return emp

    