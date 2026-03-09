from fastapi import FastAPI, HTTPException, Path, Query, Body
from contextlib import asynccontextmanager
from .db_manage import init, emp_attendance_dict, insert_att, check_date
from typing import Annotated
from .model import Attendance
import datetime
@asynccontextmanager
async def lifespan(app: FastAPI):
  init()
  print("Table Attendance Created")
  yield
  print("Shutting Down...")
  
app = FastAPI(lifespan = lifespan)
@app.get("/attendance")
async def for_emp_attendance():
  res = emp_attendance_dict()
  if res == 1:
    raise HTTPException(status_code=404)
  return res

@app.post("/attendance")
async def insert_api(att: Annotated[list[Attendance], Body()]):
  att = [i.model_dump() for i in att]
  insert_att(att)

@app.get("/date")
async def check_date_api(date: datetime.date):
  res = check_date(date)
  if res:
    raise HTTPException(status_code=409)
    
