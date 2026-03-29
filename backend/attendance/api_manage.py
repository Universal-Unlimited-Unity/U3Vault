from fastapi import HTTPException, Path, Query, Body, Response, APIRouter, Header
from contextlib import asynccontextmanager
from .db_manage import (
    emp_attendance_dict,
    insert_att,
    check_date,
    record_all,
    record_one,
    att_global_analytics,
    att_one_analytics,
    plot_status_trend_global,
    generate_all_employees_report,
    generate_single_employee_report,
    pie_plot
)
from typing import Annotated
from .model import Attendance
import datetime
from uuid import UUID
from shared.func import lazy
router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.get("/")
async def for_emp_attendance():
    res = emp_attendance_dict()
    if res == 1:
        raise HTTPException(status_code=404)
    return res


@router.post("/")
async def insert_api(att: Annotated[list[Attendance], Body()]):
    att = [i.model_dump() for i in att]
    insert_att(att)


@router.get("/date")
async def check_date_api(date: datetime.date = Query(...)):
    res = check_date(date)
    if res:
        raise HTTPException(status_code=409)


@router.get("/records")
async def att_record_all(
    start: Annotated[str | None, Query()] = None,
    end: Annotated[str | None, Query()] = None,
):
    df = record_all(start, end)
    if df.empty:
        raise HTTPException(status_code=404, detail="No Result For this period of time")
    return df.to_dict(orient="records")


@router.get("/analytics/reports")
async def att_report_all(
    status: Annotated[str, Query()],
    start: Annotated[str | None, Query()] = None,
    end: Annotated[str | None, Query()] = None,
):
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


@router.get("/analytics")
async def att_analytics_all(
    start: Annotated[str | None, Query()] = None,
    end: Annotated[str | None, Query()] = None,
):
    df = att_global_analytics(start, end)

    if df.empty:
        raise HTTPException(status_code=404, detail="No Result For this period of time")

    return df.to_dict(orient="records")


@router.get("/analytics/plots")
async def att_plots(
    status: Annotated[str, Query()],
    start: Annotated[str | None, Query()] = None,
    end: Annotated[str | None, Query()] = None,
):
    vf = plot_status_trend_global(status, start, end)
    return Response(content=vf, media_type="image/png")


@router.get("/records/{id}")
async def att_record_one(
    id: Annotated[UUID, Path()],
    auth: Annotated[str, Header()],
    start: Annotated[str | None, Query()] = None,
    end: Annotated[str | None, Query()] = None
):
    df = record_one(id, start, end)

    if df.empty:
        raise HTTPException(status_code=404, detail="No Result For this period of time")

    return df.to_dict(orient="records")

@router.get("/analytics/piechart/{id}")
async def att_piechar(id: Annotated[UUID, Path()],
                    auth: Annotated[str, Header()],
                    start: Annotated[str | None, Query()] = None,
                    end: Annotated[str | None, Query()] = None
):
    user = lazy(auth)
    if not user["role"] == "Employee":
        raise HTTPException(status_code=401)
    vf = pie_plot(id, start, end)
    return Response(content=vf, media_type="image/png")
    
@router.get("/analytics/{id}")
async def att_analytics_one(
    id: Annotated[str, Path()],
    start: Annotated[str | None, Query()] = None,
    end: Annotated[str | None, Query()] = None,
):
    df = att_one_analytics(id, start, end)

    if df.empty:
        raise HTTPException(status_code=404, detail="No Result For this period of time")

    return df.to_dict(orient="records")


@router.get("/analytics/reports/{id}")
async def att_report_one(
    full_name: Annotated[str, Query()],
    id: Annotated[str, Path()],
    start: Annotated[str | None, Query()] = None,
    end: Annotated[str | None, Query()] = None,
):
    df = att_one_analytics(id, start, end)

    if df.empty:
        raise HTTPException(status_code=404, detail="No Result For this period of time")

    return Response(
        content=generate_single_employee_report(full_name, id, df, start, end),
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="attendance_report.pdf"'},
    )
