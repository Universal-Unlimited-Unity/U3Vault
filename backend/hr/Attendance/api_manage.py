from fastapi import FastAPI, HTTPException, Path, Query, Body, Response
from contextlib import asynccontextmanager
from .db_manage import init, emp_attendance_dict, insert_att, check_date, record_all, record_one, att_global_analytics, att_one_analytics, plot_status_trend_global, generate_all_employees_report, generate_single_employee_report
from typing import Annotated
from .model import Attendance
import datetime
from uuid import UUID

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
async def check_date_api(date: datetime.date = Query(...)):
  res = check_date(date)
  if res:
    raise HTTPException(status_code=409)

@app.get("/attendance/records")
async def att_record(start: Annotated[str | None, Query()] = None, end: Annotated[str | None, Query()] = None):
  df = record_all(start, end)
  if df.empty:
    raise HTTPException(status_code=404, detail="No Result For this period of time")
  return df.to_dict(orient="records")

@app.get("/attendance/records/{id}")
async def att_record(id: Annotated[UUID, Path()], start: Annotated[str | None, Query()] = None, end: Annotated[str | None, Query()] = None):
  df = record_one(id, start, end)
  if df.empty:
    raise HTTPException(status_code=404, detail="No Result For this period of time")
  return df.to_dict(orient="records")

@app.get("/attendance/analytics")
async def att_analytics(start: Annotated[str | None, Query()] = None, end: Annotated[str | None, Query()] = None):
  df = att_global_analytics(start, end)
  if df.empty:
    raise HTTPException(status_code=404, detail="No Result For this period of time")
  return df.to_dict(orient="records")

@app.get("/attendance/analytics/{id}")
async def att_analytics(id: Annotated[str, Path()], start: Annotated[str | None, Query()] = None, end: Annotated[str | None, Query()] = None):
  df = att_one_analytics(id, start, end)
  if df.empty:
    raise HTTPException(status_code=404, detail="No Result For this period of time")
  return df.to_dict(orient="records")

@app.get("/attendance/analytics/plots")
async def att_plots(status: Annotated[str, Query()], start: Annotated[str | None, Query()] = None, end: Annotated[str | None, Query()] = None):
  vf = plot_status_trend_global(status, start, end)
  return Response(content=vf, media_type="image/png")

from fastapi import Query, HTTPException
from fastapi.responses import Response
from typing import Annotated

@app.get("/attendance/analytics/reports")
async def att_report(status: Annotated[str, Query()], start: Annotated[str | None, Query()] = None, end: Annotated[str | None, Query()] = None,):
    df = att_global_analytics(start, end)
    if df.empty:
        raise HTTPException(status_code=404, detail="No Result For this period of time")

    vf = plot_status_trend_global(status, start, end)
    pdf_bytes = generate_all_employees_report(df, vf, start, end)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="attendance_report.pdf"'},
    )

@app.get("/attendance/analytics/reports/{id}")
async def att_report(full_name: Annotated[str, Query()], id: Annotated[str, Path()], start: Annotated[str | None, Query()] = None, end: Annotated[str | None, Query()] = None):
  df = att_one_analytics(id, start, end)
  if df.empty:
    raise HTTPException(status_code=404, detail="No Result For this period of time")
  return Response(
        content = generate_single_employee_report(full_name, id, df, start, end),
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="attendance_report.pdf"'},
    )
