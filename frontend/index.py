import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
import requests
#from dotenv import load_dotenv
import os
from uuid import uuid4
from datetime import date
#load_dotenv()
#API_URL = os.getenv("API_URL")


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

#SideBar

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
    
#MainPage

if st.session_state.page == "Human Resources/Employees":
    col1, col2 = st.columns([1,2])

    with col1:
        st.image("front.png", width=720)

    add, delete, update, listall, showprofile = st.tabs([
        "Add Employee", "Delete Employee", "Update Employee", "List Employees", "Employee Profile"
    ])

    with add:
        # We need logic to maake form go off when submit is clicked later
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
            emp = {
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
                response = requests.post(API_URL, json=emp)
                
                if response.status_code == 200:
                    st.success("Employee Added Successfully!")
                    result = response.json()
                    with st.spinner("Loading Employee's infos..."):
                        st.dataframe(result)
                        if st.button("Add New Employee"):
                            st.rerun()
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
                
    with delete:
            
        try: 
            with st.spinner("Loading Employees's List..."):
                result = requests.get(API_URL)
            
            if result.status_code == 200:
                data = result.json()
                to_delete = st.selectbox(
                    "Select or Search Employee",
                    options=list(data.keys()), 
                    format_func=lambda x: data[x]
                )
                
                if st.button("Confirm Deletion", use_container_width=True):
                    with st.spinner("Deleting..."):
                        deleted = requests.delete(f"{API_URL}/{to_delete}")
                    
                    if deleted.status_code == 200:
                        st.success("Employee Deleted Successfully!")
                        st.info("Info of Deleted Employee:")
                        st.dataframe(deleted.json())
                        
                        if st.button("Clear and Refresh"):
                            st.rerun()
                                    
                    elif deleted.status_code == 404:
                        st.error("Error: Could not find employee to delete.")
                
            elif result.status_code == 404:
                st.warning("No employees found in the database.")
                
        except Exception as e:
            st.error(f"Backend Error: {e}")

    with listall:
        try:
            with st.spinner("Loading Employees's Full List"):
                
                response = requests.get(f"{API_URL}/dataframe")
            if response.status_code == 200:
                result = response.json()
                st.dataframe([result])
            elif response.status_code == 404:
                st.warning("No employees found in the database.")
        except Exception as e:
            st.error(f"Backend Error: {e}")
    
    with showprofile:
            
        try: 
            with st.spinner("Loading Employees's List..."):
                result = requests.get(API_URL)
            
            if result.status_code == 200:
                data = result.json()
                to_show = st.selectbox(
                    "Select or Search Employee",
                    options=list(data.keys()), 
                    format_func=lambda x: data[x]
                )
                
                if st.button("Show Employee's Profil", use_container_width=True):
                    with st.spinner("Getting Employye's Profil..."):
                        emp = requests.get(f"{API_URL}/{to_show}")
                    
                    if emp.status_code == 200:
                        
                    
                        if st.button("Clear and Refresh"):
                            st.rerun()
                                    
                    elif emp.status_code == 404:
                        st.error(f"Error")
                
            elif result.status_code == 404:
                st.warning("No employees found in the database.")
                
        except Exception as e:
            st.error(f"Backend Error: {e}")
    
        