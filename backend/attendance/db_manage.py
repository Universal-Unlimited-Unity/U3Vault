from sqlalchemy import MetaData, Table, Column, ForeignKey, String, Date, select, insert
from db.db_connect import db_connect, metadata
from datetime import date
from sqlalchemy.dialects.postgresql import UUID
from employees.db_manage import employees
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import tempfile
import os
from fpdf import FPDF
from uuid import UUID as UUID_type
eng = db_connect()

attendance = Table(
    "attendance",
    metadata,
    Column("id", UUID(as_uuid=True), nullable=True),
    Column("first_name", String, nullable=False),
    Column("middle_name", String, nullable=True),
    Column("last_name", String, nullable=False),
    Column("date", Date, nullable=False),
    Column("status", String, nullable=False)
)

def init() -> None:
    metadata.create_all(eng, checkfirst=True)

def emp_attendance_dict():
    with eng.connect() as conn:
        stmt = select(employees)
        emps = conn.execute(stmt).mappings().fetchall()
        if not emps:
            return 1
        newhash = {}
        for i in emps:
            middle_name = i["middle_name"] if i["middle_name"] else ""
            newhash[str(i["id"])] = {"id": str(i["id"]), "first_name": i["first_name"], "middle_name": middle_name, "last_name": i["last_name"], "status":"", "date": ""}
        return newhash
        
def insert_att(att: list[dict[str, str]]):
    with eng.connect() as conn:
        conn.execute(insert(attendance), att)
        conn.commit()

def check_date(att_date: date):
    with eng.connect() as conn:
        stmt = select(attendance).where(attendance.c.date == att_date)
        res = conn.execute(stmt).fetchone()
        return res

def att_dataframe_all():
    df = pd.read_sql_table("attendance", eng)
    df.columns = df.columns.map(str)
    df["date"] = pd.to_datetime(df["date"])
    return df

def att_dataframe_one(id: UUID_type):
    df = att_dataframe_all()
    df = df[df["id"] == id]
    return df

def record_all(start: str = None, end: str = None):
    df = att_dataframe_all()
    if start and end:
        df = timeperiod(df, start, end)
    return df
    
def record_one(id: UUID_type, start: str = None, end: str = None):
    df = att_dataframe_one(id)
    if start or end:
        df = timeperiod(df, start, end)
    return df
    
def timeperiod(df: pd.DataFrame, start: str, end: str):
    if start:
        start = pd.to_datetime(start)
        df = df[df["date"] >= start]
    if end:
        end = pd.to_datetime(end)
        df = df[df["date"] <= end]
    return df
def att_global_analytics(start: str=None, end: str=None):
    df = att_dataframe_all()
    df = timeperiod(df, start, end)
    df = (df["status"].value_counts(normalize=True)*100).reset_index(name="Percentage")
    df = df.rename(columns={"status": "Status"})
    return df

def att_one_analytics(id: str, start=None, end=None):
    df = record_one(id, start, end)
    df = (df["status"].value_counts(normalize=True)*100).reset_index(name="Percentage")
    df = df.rename(columns={"status": "Status"})
    return df

def _help_plot_status_trend_global(start: str, end: str):
    df = att_dataframe_all()
    df = timeperiod(df, start, end)
    df = (df.groupby("date")["status"].value_counts(normalize=True)*100).reset_index(name="Percentage")
    return df
def plot_status_trend_global(status: str, start: str = None, end : str = None):
    df = _help_plot_status_trend_global(start, end)

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values("date")

    fig, ax = plt.subplots(figsize=(15, 5))
    vf = BytesIO()

    if status != "All":
        df = df[df["status"] == status]
        if len(df) >= 10:
            sns.lineplot(data=df, x="date", y="Percentage", ax=ax)
        else:
            sns.lineplot(data=df, x="date", y="Percentage", ax=ax, marker='o')
    else:
        if len(df) >= 10:
            sns.lineplot(data=df, x="date", y="Percentage", hue="status")
        else:
            sns.lineplot(data=df, x="date", y="Percentage", hue="status", ax=ax, marker='o')

    fig.savefig(vf, format="png", bbox_inches="tight")
    plt.close(fig)

    vf.seek(0)
    return vf.read()

def pie_plot(id: UUID_type, start: str, end: str):
    df = att_one_analytics(id, start, end)
    labels = df["Status"]
    sizes = df["Percentage"]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.0f%%", startangle=90)
    ax.axis("equal")
    vf = BytesIO()
    fig.savefig(vf, format="png")
    plt.close(fig)
    vf.seek(0)
    return vf.read()

def pie_plot2(start: str, end: str):
    df = att_global_analytics(start, end)
    labels = df["Status"]
    sizes = df["Percentage"]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.0f%%", startangle=90)
    ax.axis("equal")
    vf = BytesIO()
    fig.savefig(vf, format="png")
    plt.close(fig)
    vf.seek(0)
    return vf.read()

