from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from .db_manage import init, emp_attendance_dict
@asynccontextmanager
async def lifespan(app: FastAPI):
  init()
  print("Table Attendance Created")
  yield
  print("Shutting Down...")
  
app = FastAPI(lifespan = lifespan)
@app.get("/attendace")
async def for_emp_attendance()
  res = emp_attendance_dict()
  if res = 1:
    raise HTTPException(status_code=404)
  return res
    
