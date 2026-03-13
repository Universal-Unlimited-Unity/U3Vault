import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
import requests
from dotenv import load_dotenv
import os
import base64
from uuid import uuid4
from datetime import date
from model import Employee

load_dotenv()
API_URL = os.getenv("API_URL")
API_URL_att = os.getenv("API_URL_att")
API_URL_date = os.getenv("API_URL_date")
def save_upload(upload: UploadedFile, dir: str) -> str | None:
    if upload is None:
        return None
    root = os.getenv("UPLOADS_ROOT", "/myapp/uploads")
    upload_dir = os.path.join(root, dir)
    os.makedirs(upload_dir, mode=0o755, exist_ok=True)
    ext = upload.name.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    path = os.path.join(upload_dir, filename)
    with open(path, "wb") as f:
        f.write(upload.getbuffer())
    return f"{dir}/{filename}"  
    
st.set_page_config(page_icon="logoo.png", page_title="U3Vault")

st.sidebar.title("Navigation")

if "page" not in st.session_state:
    st.session_state.page = "home"

with st.sidebar.expander("Human Resources"):
    if st.button("Employees", use_container_width=True):
        st.session_state.page = "Human Resources/Employees"
    if st.button("Attendance", use_container_width=True):
        st.session_state.page = "Human Resources/Attendance"
    if st.button("Leave Management", use_container_width=True):
        st.session_state.page = "Human Resources/Leave Management"
    if st.button("Payroll", use_container_width=True):
        st.session_state.page = "Human Resources/Payroll"

with st.sidebar.expander("Contracts"):
    st.button("y")
    
with st.sidebar.expander("Organization"):
    st.button("p")

with st.sidebar.expander("Documents"):
    st.button("d")
    
with st.sidebar.expander("Requests"):
    st.button("z")
    
with st.sidebar.expander("Reports"):
    st.button("f")
    
with st.sidebar.expander("Administration"):
    st.button("q")
    
with st.sidebar.expander("Settings"):
    st.button("c")

if st.session_state.page == "Human Resources/Employees":
    col1, col2 = st.columns([1,2])

    with col1:
        st.image("front.png", width=720)

    add, delete, update, listall, showprofile = st.tabs([
        "Add Employee", "Delete Employee", "Update Employee", "List Employees", "Employee Profile"
    ])

    with add:
        with st.form("add_employee_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name")
                middle_name = st.text_input("Middle Name (Optional)")
                last_name = st.text_input("Last Name")
                gender = st.selectbox("Gender", ["Male", "Female"])
                dob = st.date_input("Date of Birth", min_value=date(1900, 1, 1))
                phone = st.text_input("Phone Number")
                email = st.text_input("Email")
                address = st.text_area("Address")
                photo = st.file_uploader("Upload Photo", type=["png", "jpg", "jpeg"])
            with col2:
                department = st.text_input("Department")
                role = st.text_input("Job Title / Role")
                supervisor = st.text_input("Supervisor")
                employment_type = st.selectbox("Employment Type", ["Full-time", "Part-time"])
                start_date = st.date_input("Start Date")
                status = st.selectbox("Status", ["Active", "On Leave", "Inactive", "Resigned"])
                contract_type = st.selectbox("Contract Type", ["Employee", "Temporary", "Intern"])
                contract_pdf = st.file_uploader("Upload Contract PDF", type=["pdf"])
                emergency_phone = st.text_input("Emergency Contact Phone (Optional)")
            submit = st.form_submit_button("Add Employee")

        if submit:
            emp_payload = {
                "first_name": first_name.title(),
                "middle_name": middle_name.title() if middle_name else None,
                "last_name": last_name.title(),
                "gender": gender, 
                "dob": str(dob),
                "phone": phone,
                "email": email,
                "address": address,
                "photo": save_upload(photo, "uploads/photos"), 
                "department": department,
                "role": role,
                "supervisor": supervisor if supervisor else None,
                "employment_type": employment_type,       
                "start_date": str(start_date),
                "status": status,
                "contract_type": contract_type,
                "contract_pdf": save_upload(contract_pdf, "uploads/contracts"), 
                "emergency_phone": emergency_phone if emergency_phone else None
            }
            try:
                response = requests.post(API_URL, json=emp_payload)
                if response.status_code == 200:
                    st.success("Employee Added Successfully!")
                    st.dataframe(response.json())
            except Exception as e:
                st.error(f"Error: {e}")
                
    with delete:
        try: 
            result = requests.get(API_URL)
            if result.status_code == 200:
                data = result.json()
                to_delete = st.selectbox(
                    "Select Employee",
                    options=list(data.keys()), 
                    format_func=lambda x: data[x],
                    key="del_select"
                )
                if st.button("Confirm Deletion", use_container_width=True, key="del_confirm"):
                    deleted = requests.delete(f"{API_URL}/{to_delete}")
                    if deleted.status_code == 200:
                        st.success("Employee Deleted Successfully!")
                        st.info("Info of Deleted Employee:")
                        st.dataframe(deleted.json())
                        if st.button("Clear and Refresh"):
                            st.rerun()
            elif result.status_code == 404:
                st.warning("No employees found in the database.")               
        except Exception as e:
            st.error(f"Error: {e}")

    with listall:
        try:
            response = requests.get(f"{API_URL}/dataframe")
            if response.status_code == 200:
                st.dataframe(response.json())
            elif response.status_code == 404:
                st.warning("No employees found in the database.")

        except Exception as e:
            st.error(f"Error: {e}")
    
    with showprofile:
        try: 
            result = requests.get(API_URL)
            if result.status_code == 200:
                data = result.json()
                to_show = st.selectbox(
                    "Select Employee",
                    options=list(data.keys()), 
                    format_func=lambda x: data[x],
                    key="prof_select"
                )
                
                if st.button("Show Profile", use_container_width=True, key="prof_btn"):
                    emp_api = requests.get(f"{API_URL}/{to_show}")
                    if emp_api.status_code == 200:
                        root = os.getenv("UPLOADS_ROOT", "/myapp/uploads")
                        emp = Employee(**emp_api.json())
                        emp.photo = os.path.join(root, emp.photo)
                        pdf_path = os.path.join(root, emp.contract_pdf)

                        st.markdown("### Employee Profile")
                        c1, c2 = st.columns([1, 3])
                        with c1:
                            st.image(emp.photo, use_container_width=True)
                            st.write(f"**Status:** {emp.status.value}")
                        with c2:
                            st.header(f"{emp.first_name} {emp.last_name}")
                            st.caption(f"{emp.role} | {emp.department}")
                            st.write(f"**Email:** {emp.email}")
                            st.write(f"**Phone:** {emp.phone}")
                            st.divider()
                            
                            with open(pdf_path, "rb") as f:
                                b64_pdf = base64.b64encode(f.read()).decode('utf-8')
                            
                            pdf_view = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
                            st.markdown(pdf_view, unsafe_allow_html=True)
                            st.download_button("Download PDF", base64.b64decode(b64_pdf), f"contract_{emp.id}.pdf", "application/pdf", key=f"dl_{emp.id}")
                                            
                        if st.button("Refresh", key=f"re_{emp.id}"):
                            st.rerun()
            elif result.status_code == 404:
                st.warning("No employees found in the database.")
        except Exception as e:
            st.error(f"Error: {e}")
if st.session_state.page == "Human Resources/Attendance":
    # we need to really understand this code and anlyze it and we need sucess logic to work
    if "case" not in st.session_state:
        st.session_state.case = False
    if "emps" not in st.session_state:
        st.session_state.emps = {}
    if "check" not in st.session_state:
        st.session_state.check = False
    
    daily, records, analytics = st.tabs(["Today's Attendance", "Attendance Records", "Analytics"])

    with daily:
        today = date.today().isoformat()
        query = {"date": today}
        
        try:
            check = requests.get(API_URL_date, params=query)
            if check.status_code == 409:
                st.warning("Attendance for today has already been recorded. To prevent fraud and ensure data integrity, the system is locked for new entries until tomorrow.")
                if st.button("Refresh"):
                    st.rerun()
            elif check.status_code == 200:
                st.session_state.check = True
        except Exception as e:
            st.error(f"Backend unavailable: {e}")
        
        if st.session_state.check:
            if not st.session_state.emps:
                try:
                    res = requests.get(API_URL_att)
                    if res.status_code == 404:
                        st.error("The DataBase is Empty!")
                    elif res.status_code == 200:
                        st.session_state.emps = res.json()
                        st.session_state.case = True       
                except Exception as e:
                    st.error(f"Backend unavailable: {e}")
            
            if st.session_state.case:
                st.info(f"Recording attendance for {today}")
                with st.form("attendance_submission"):
                    for id, info in st.session_state.emps.items():
                        full_name = f"{info['first_name']} {info['middle_name']} {info['last_name']}"
                        name, status = st.columns(2)
                        with name:
                            st.write(full_name)
                        with status:
                            s = st.selectbox("Status", options=["Remote", "Vacation", "Sick", "Absent", "Present"], key=id)
                            st.session_state.emps[id]["status"] = s
                            st.session_state.emps[id]["date"] = today
                    
                    submitted = st.form_submit_button("Submit Attendance")
                    if submitted:
                        try:
                            payload = list(st.session_state.emps.values())
                            res = requests.post(API_URL_att, json=payload)
                            if res.status_code == 200:
                                st.success("Attendance recorded successfully.")
                                st.session_state.emps = {}
                                st.session_state.check = False
                                st.rerun()
                            else:
                                st.error(f"Error: {res.text}")
                        except Exception as e:
                            st.error(f"Error: {e}")
    with records:
        radio = st.radio("View Scope", options=["Single Employee", "All Employees"], horizontal=True)
        if radio == "Single Employee":
            try: 
                result = requests.get(API_URL)
                if result.status_code == 200:
                    data = result.json()
                    id = st.selectbox(
                        "Select Employee",
                        options=list(data.keys()), 
                        format_func=lambda x: data[x],
                        key="record_select"
                    )
                    col1, col2 = st.columns(2)
                    st.markdown("Enter Start and End Date of the Records, To Show All Time Records Leave Them Empty")
                    st.markdown("This is an MVP, If You Enter One and Leave Another Empty The Result Would Be All The Time")
                    with col1:
                        start = st.date_input("Start Date", min_value=date(2010, 1, 1), value=None, key="start")
                    with col2:
                        end = st.date_input("Start Date", min_value=date(2010, 1, 1), value=None, key="end")
                    if st.button("Show Records"):
                        if start and end:
                            payload = {"start": str(start), "end": str(end)}
                            try:
                                record = requests.get(f"{API_URL_att}/records/{id}", params=payload)
                            except Exception as e:
                                st.error(f"Error: {e}")
                        else:
                            try:
                                record = requests.get(f"{API_URL_att}/records/{id}")
                            except Exception as e:
                                st.error(f"Error: {e}")
                        if record.status_code == 200:
                            pre_df = record.json()
                            st.dataframe(pre_df)
                        elif record.status_code == 404:
                            st.warning("No Records For This Employee In This Time Period")
                        if st.button("Refresh", key="refresh"):
                            st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
        if radio == "All Employees":
            
            col1, col2 = st.columns(2)
            st.markdown("Enter Start and End Date of the Records, To Show All Time Records Leave Them Empty")
            st.markdown("This is an MVP, If You Enter One and Leave Another Empty The Result Would Be All The Time")
            with col1:
                start = st.date_input("Start Date", min_value=date(2010, 1, 1), value=None, key="start")
            with col2:
                end = st.date_input("Start Date", min_value=date(2010, 1, 1), value=None, key="end")
            if st.button("Show Records"):
                if start and end:
                    payload = {"start": str(start), "end": str(end)}
                    try:
                        record = requests.get(f"{API_URL_att}/records", params=payload)
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    try:
                        record = requests.get(f"{API_URL_att}/records")
                    except Exception as e:
                        st.error(f"Error: {e}")
                if record.status_code == 200:
                    pre_df = record.json()
                    st.dataframe(pre_df)
                elif record.status_code == 404:
                    st.warning("No Records For This Time Period")
                if st.button("Refresh", key="refresh"):
                    st.rerun()
    with analytics:
        radio = st.radio("View Scope", options=["Single Employee", "All Employees"], horizontal=True)
        if radio == "Single Employee":
            if "start_o" not in st.session_state:
                st.session_state.start_o = None
            if "end_o" not in st.session_state:
                st.session_state.end_o = None
            if "id_o" not in st.session_state:
                st.session_state.id_o = None
            if "data_o" not in st.session_state:
                st.session_state.data_o = None                
            try: 
                result = requests.get(API_URL)
                if result.status_code == 200:
                    st.session_state.data_o = result.json()
                    st.session_state.id_o = st.selectbox(
                        "Select Employee",
                        options=list(data.keys()), 
                        format_func=lambda x: data[x],
                        key="record_select"
                    )
                    col1, col2 = st.columns(2)
                    st.markdown("Enter Start and End Date of the Records, To Show All Time Records Leave Them Empty")
                    st.markdown("This is an MVP, If You Enter One and Leave Another Empty The Result Would Be All The Time")
                    with col1:
                        st.session_state.start_o = st.date_input("Start Date", min_value=date(2010, 1, 1), value=None, key="start")
                    with col2:
                        st.session_state.end_o = st.date_input("Start Date", min_value=date(2010, 1, 1), value=None, key="end")
                    if st.button("Show Analytics"):
                        if st.session_state.start_o and st.session_state.end_o:
                            payload = {"start": str(st.session_state.start_o), "end": str(st.session_state.end_o)}
                            try:
                                record = requests.get(f"{API_URL_att}/analytics/{st.session_state.id_o}", params=payload)
                            except Exception as e:
                                st.error(f"Error: {e}")
                        else:
                            try:
                                record = requests.get(f"{API_URL_att}/analytics/{st.session_state.id_o}")
                            except Exception as e:
                                st.error(f"Error: {e}")
                        if record.status_code == 200:
                            pre_df = record.json()
                            st.dataframe(pre_df)
                            if st.button("Generate Report As PDF"):
                                if st.session_state.start_o and st.session_state.end_o:
                                    full_name = f"{st.session_state.data_o[st.session_state.id_o]["full_name"]}{st.session_state_data_o[st.session_state.id_o]["middle_name"]}{st.session_state.data_o[st.session_state.id_o]["last_name"]}"
                                    payload = {"full_name": full_name, "start": str(st.session_state.start_o), "end": str(st.session_state.end_o}}
                                    try:
                                        report = requests.get(f"{API_URL_att}/analytics/reports/{st.session_state.id_o}", params=payload)
                                    except Exception as e:
                                        st.error(f"Error: {e}")
                                else:
                                    full_name = f"{st.session_state.data_o[st.session_state.id_o]["full_name"]}{st.session_state_data_o[st.session_state.id_o]["middle_name"]}{st.session_state.data_o[st.session_state.id_o]["last_name"]}"
                                    payload = {"full_name": full_name}
                                    try:
                                        report = requests.get(f"{API_URL_att}/analytics/reports/{st.session_state.id_o}", params=payload)
                                    except Exception as e:
                                        st.error(f"Error: {e}")
                                        
                                if report.status_code == 200:

                                    pdf_bytes = report.content
                                    b64_report = base64.b64encode(pdf_bytes).decode("utf-8")

                                    st.markdown(
                                        f"""
                                        <iframe
                                            src="data:application/pdf;base64,{b64_report}"
                                            width="700"
                                            height="900"
                                            type="application/pdf">
                                        </iframe>
                                        """,
                                        unsafe_allow_html=True,
                                    )

                                    st.download_button(
                                        label="Download employee report (PDF)",
                                        data=pdf_bytes,
                                        file_name=f"attendance_{st.session_state.id_}_{st.session_state.start_o}_{st.session_state.end}.pdf",
                                        mime="application/pdf",
                                    )
                                elif repor.status_code == 404:
                                    st.error("Something Went Wrong...")
                        elif record.status_code == 404:
                            st.warning("No Records For This Employee In This Time Period")
        
                        if st.button("Refresh", key="refresh"):
                            st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
        if radio == "All Employees":
            if "start" not in st.session_state:
                st.session_state.end = None
            if "end" not in st.session_state:
                st.session_state.end = None
            if "status" not in st.session_state:
                st.session_state.status = None
            col1, col2 = st.columns(2)
            st.markdown("Enter Start and End Date of the Records, To Show All Time Records Leave Them Empty")
            st.markdown("This is an MVP, If You Enter One and Leave Another Empty The Result Would Be All The Time")
            with col1:
                st.session_state.start = st.date_input("Start Date", min_value=date(2010, 1, 1), value=None, key="start")
            with col2:
                st.session_state.end = st.date_input("Start Date", min_value=date(2010, 1, 1), value=None, key="end")
            if st.button("Show Analytics"):
                if st.session_state.start and st.session_state.end:
                    payload = {"start": str(st.session_state.start), "end": str(st.session_state.end)}
                    try:
                        record = requests.get(f"{API_URL_att}/analytics", params=payload)
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    try:
                        record = requests.get(f"{API_URL_att}/analytics")
                    except Exception as e:
                        st.error(f"Error: {e}")
                if record.status_code == 200:
                    pre_df = record.json()
                    st.dataframe(pre_df)
                elif record.status_code == 404:
                    st.warning("No Records For This Time Period")
                if st.button("Generate Plot (Graph)"):
                    st.session_state.status = st.selectbox("Chose Which Status To Plot Over Time Or Chose All To Plot All Status", options=["Remote", "Vacation", "Sick", "Absent", "Present"])
                    if st.session_state.start and st.session_state.end:
                        payload = {"status": st.session_state.status, "start": str(st.session_state.start), "end": str(st.session_state.end}}
                        try:
                            plot = requests.get(f"{API_URL_att}/analytics/plots/", params=payload)
                        except Exception as e:
                            st.error(f"Error: {e}")
                    else:
                        payload = {"status": st.session_state.status}
                        try:
                            plot = requests.get(f"{API_URL_att}/analytics/plots/", params=payload)
                        except Exception as e:
                            st.error(f"Error: {e}")
                    if plot.status_code == 200:
                        st.image(plot.content, use_container_width=True)
                        if st.button("Generate Report"):
                if st.button("Refresh", key="refresh"):
                    st.rerun()
