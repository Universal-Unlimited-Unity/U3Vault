from fastapi import FastAPI
from create_company.api_manage import router as company_router
from auth.api_manage import router as auth_router
from attendance.api_manage import router as attendance_router
from employees.api_manage import router as employees_router
from contextlib import asynccontextmanager
from create_company.db_manage import init as comp_init
from employees.db_manage import init as emp_init
from attendance.db_manage import init as att_init
from leave_req.api_manage import router as request_router
from leave_req.db_manage import init as req_init
@asynccontextmanager
async def lifespan(app: FastAPI):
  print("Database Started Seccussfully")
  comp_init()
  emp_init()
  att_init()
  req_init()
  yield
  print("Shutting Down...")
  
app = FastAPI(lifespan=lifespan)

app.include_router(company_router)
app.include_router(auth_router)
app.include_router(attendance_router)
app.include_router(employees_router)
app.include_router(request_router)
