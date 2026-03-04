from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db_manage import init, add
from .model import Employee
asynccontextmanager
async def lifespan(app: FastAPI):
    init()
    print("Employee Table Created!")
    yield
    print("Shutting Down...")    
    
app = FastAPI(lifespan=lifespan)

app.post("/employees", response_model=Employee)
async def add(emp: Employee) -> Employee:
    return add(emp)

    