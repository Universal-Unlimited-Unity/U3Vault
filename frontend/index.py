import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
import requests
from dotenv import load_dotenv
import os
import base64
from uuid import uuid4
from datetime import date
from model import Employee, Employee_s
import time
from jose import jwt
load_dotenv()
API_URL = os.getenv("API_URL")
API_URL_att = os.getenv("API_URL_att")
API_URL_date = os.getenv("API_URL_date")
API_URL_AUTH = os.getenv("API_URL_AUTH")
API_URL_COMP = os.getenv("API_URL_COMP")
TOKEN_KEY = os.getenv("TOKEN_KEY")
ALGO = os.getenv("ALGO")
root = os.getenv("UPLOADS_ROOT", "/myapp/uploads/")
API_URL_REQ = os.getenv("API_URL_REQ")

def save_upload(upload: UploadedFile, dir: str) -> str | None:
    if upload is None:
        return None
    upload_dir = os.path.join(root, dir)
    os.makedirs(upload_dir, mode=0o755, exist_ok=True)
    ext = upload.name.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    path = os.path.join(upload_dir, filename)
    with open(path, "wb") as f:
        f.write(upload.getbuffer())
    return f"{dir}/{filename}"  

def check_pwd(pwd):
    if len(pwd) >= 10 and any(c.islower() for c in pwd) and any(c.isupper() for c in pwd) and any(c.isdigit() for c in pwd):
        return True
    else:
        return False
st.set_page_config(page_icon="logoo.png", page_title="U3Vault")

# sign-in/sign-up
if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    st.session_state.choice = st.radio("Chose An Action", ["Create Company Account", "Login"])
    if st.session_state.choice == "Login":
        st.title("Welcome Back")
        st.session_state.role = st.selectbox("Login Type", options=["Admin", "Manager/Employee"], width='stretch')
        if st.session_state.role == "Manager/Employee":
            with st.form("Login", clear_on_submit=True):
                slug = st.text_input("Company Slug")
                email = st.text_input("Email")
                pwd = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", width='stretch')
            if submit:
                if all([slug, email, pwd]):
                    payload = {"role": st.session_state.role,
                            "slug": slug,
                            "email": email,
                            "password": pwd
                            }
                    try:
                        res = requests.post(f"{API_URL_AUTH}/login", json=payload)
                        if res.status_code == 200:
                            st.session_state.token = res.json()["token"]
                            st.session_state.headers = {"auth": f"Bearer {st.session_state.token}"}
                            st.session_state.logged = True
                            st.rerun()
                        elif res.status_code == 401:
                            st.error("Wrong Infos")
                    except Exception as e:
                        st.error(f"Backend Error {res.text}")
                else:
                    st.error("You Must Enter All Fields")
        else:
            with st.form("Login", clear_on_submit=True):
                email = st.text_input("Email")
                pwd = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", width='stretch')
            if submit:
                if all([email, pwd]):
                    payload = {"role": st.session_state.role,
                            "email": email,
                            "password": pwd}
                    try:
                        res = requests.post(f"{API_URL_AUTH}/login", json=payload)
                        if res.status_code == 200:
                            st.session_state.token = res.json()["token"]
                            st.session_state.headers = {"auth": f"Bearer {st.session_state.token}"}
                            st.session_state.logged = True
                            st.rerun()
                        elif res.status_code == 401:
                            st.error("Wrong Infos")
                    except Exception as e:
                        st.error(f"Backend Error {e}")
                else:
                    st.error("You Must Enter All Fields")
    else:
        st.title("Create Your Company")
        with st.form("Enter Your Company's Infos", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Company Name")
                phone = st.text_input("Phone Number")
                password1 = st.text_input("Password", type='password')
            with col2:
                email = st.text_input("Email")
                address = st.text_input("Address")
                password2 = st.text_input("Renter Your Password", type='password')
            if st.form_submit_button("Create Company", width='stretch'):
                if all([name, phone, password1, email, address, password2]):
                    if password1 == password2:
                        if not check_pwd(password1):
                            st.error("Verification Failed: Your password must be at least 10 characters long and include a mix of uppercase letters, lowercase letters, and numbers.")                        
                        else:
                            try:
                                slug = requests.get(f"{API_URL_COMP}/{name}")
                                if slug.status_code == 200:
                                    
                                    payload = {"name": name,
                                            "phone_number": phone,
                                            "email": email,
                                            "password": password1,
                                            "address": address,
                                            "slug": slug.json()}
                                else:
                                    st.error("Backend Error")
                            except Exception as e:
                                st.error(f"Backend Error: {e}")
                            try:
                                res = requests.post(API_URL_COMP, json=payload)
                                if res.status_code == 200:
                                    st.success("Company Created! You Can Now Use Your Email And Password To Login")
                                    st.session_state.choice = "Login"
                                    st.session_state.role = "Admin"
                                elif res.status_code == 500:
                                    st.error("Couldn't Add Company")
                                elif res.status_code == 422:
                                    st.error("Make Sure You Provide a Valid Email And Your Phone have contry code: e.g +2126XXXXXXXX")
                                elif res.status_code == 409:
                                    st.error("Email Already Used")
                            except Exception as e:
                                st.error(f"Backend Error {e}")
                    else:
                        st.warning("Passwords Don't Match")
                        
                else:
                    st.warning("You Must Fill All Fields")
                    
if st.session_state.logged:
    st.session_state.user = jwt.decode(
        st.session_state.token, TOKEN_KEY, algorithms=[ALGO]
    )

    if st.session_state.user["role"] == "Employee":
        if "page" not in st.session_state:
            st.session_state.page = "Home"

        st.sidebar.image("front.png")
        st.sidebar.title("")
        
        if st.sidebar.button("Home", width='stretch'):
            st.session_state.page = "Home"
        if st.sidebar.button("Leave Requests", width='stretch'):
            st.session_state.page = "Leave Requests"
        if st.sidebar.button("Attendance", width='stretch'):
            st.session_state.page = "Attendance"
        if st.sidebar.button("Settings", width='stretch'):
            st.session_state.page = "Settings"
        if st.sidebar.button("Contract", width='stretch'):
            st.session_state.page = "Contract"
        if st.sidebar.button("🚪 Logout", width='stretch'):
            st.session_state.clear()
            st.rerun()

        if st.session_state.page == "Home":

            if "info" not in st.session_state:
                st.session_state.info = None
    
            try:
                info = requests.get(f"{API_URL}/{st.session_state.user['id']}", headers=st.session_state.headers)
                if info.status_code == 200:
                    if not st.session_state.info:
                        st.session_state.info = Employee_s(**info.json())
            except Exception as e:
                st.error(f"Backend Error {e}")
    
            if st.session_state.info:
    
                st.image("front.png", width=160)
    
                col1, col2 = st.columns([1, 3])
    
                with col1:
                    img = os.path.join(root, st.session_state.info.photo) if st.session_state.info.photo else "default.png"
                    st.image(img, width=120)
    
                with col2:
                    st.markdown(f"""
                    ## Welcome {st.session_state.info.first_name} {st.session_state.info.last_name}
                    **Role:** {st.session_state.info.role.value}
                    """)
    
                st.markdown("---")
    
                col1, col2 = st.columns(2)
    
                
                cmp_name = requests.get(API_URL_COMP, headers=st.session_state.headers)
                if cmp_name.status_code == 200:
                    st.session_state.cmp_name = cmp_name.json()
                elif cmp_name.status_code == 404:
                    st.error("Something Went Wrong")
                with col1:
                    st.info(f"📧 Email: {st.session_state.info.email}")
                    st.info(f"📱 Phone: {st.session_state.info.phone}")
    
                with col2:
                    st.info(f"🏢 Department: {st.session_state.info.department}")
                    st.info(f"Company: {st.session_state.cmp_name}")
                    
        if st.session_state.page == "Leave Requests":

            st.image("front.png", width=160)
            create_req, check_req = st.tabs(["Create Request", "Check Request"])
            with create_req:
                with st.form("Leave Request"):
                    reason = st.text_input("Reason*", placeholder="e.g. sick")
                    start_date = st.date_input("Start Date*")
                    end_date = st.date_input("End Date", value=None)
                    doc = st.file_uploader("Upload Justification*", type=["pdf"], accept_multiple_files=False)
                    submit = st.form_submit_button("Submit Request")
                if submit:
                    if not reason or not start_date or not doc:
                        st.error("Please fill out all fields marked with an asterisk (*)")
                    else:
                        payload = {"reason": reason,
                                    "start_date": str(start_date),
                                    "end_date": str(end_date),
                                    "status": "Pending",
                                    "cmp_id": st.session_state.user["company_id"],
                                    "emp_id": st.session_state.user["id"],
                                    "doc": save_upload(doc, "requests")}
                        try:
                            res = requests.post(API_URL_REQ, json=payload, headers=st.session_state.headers)
                        except Exception as e:
                            st.error(f"Backend Error: {e}")
                        if res.status_code == 200:
                            st.success("Request Submited Successfully, Check It's Status In The Other Tab")
                        elif res.status_code in ["401", "404"]:
                            st.error("Something Went Wrong")
            with check_req: 
                status = st.selectbox("Status", options=["All", "Pending", "Approved", "Rejected"])
                with st.spinner("Loading Requests"):
                    try:
                        res = requests.get(API_URL_REQ, params={"status": status}, headers=st.session_state.headers)
                    except Exception as e:
                        st.error(f"Backend Error: {e}")
                    
                    if res.status_code == 200:
                        reqs = res.json() 
                        for req in reqs:
                            col1, col2, col3 = st.columns([1, 2, 0.8])
                            with col1:
                                st.write(f"`{req['date'][:10]}`")
                            with col2:
                                st.write(req["reason"])
                            with col3:
                                s = req["status"]
                                color = "green" if s == "Approved" else "orange" if s == "Pending" else "red"
                                st.markdown(f":{color}[**{s}**]")
                            st.divider()
                    elif res.status_code == 401 or res.status_code == 404:
                        st.error("Something Went Wrong")
        if st.session_state.page == "Attendance":
            st.image("front.png", width=160)
            st.markdown(f":green[Here You Can Keep Track Of Your Attendance]")
            st.divider()
            st.markdown(f":blue[Please enter the time period you wish to check. Leave both Start and End empty to search all time, or fill only one to search from a specific date forward or backward.]")
            start = st.date_input("Start Date", value=None)
            end = st.date_input("End Date", value=None)
            if st.button("Load Attendance Records And Analytics", width='stretch'):
                query = {"start": start,
                         "end": end}
                try:
                    with st.spinner("Loading"):
                        res = requests.get(f"{API_URL_att}/records/{st.session_state.user["id"]}", params=query, headers=st.session_state.headers)
                        if res.status_code == 200:
                            df = res.json()
                            try:
                                pie = requests.get(f"{API_URL_att}/analytics/piechart/{st.session_state.user["id"]}", 
                                                    params=query, headers=st.session_state.headers)
                            
                                tab1, tab2 = st.tabs(["📋 Records", "📊 Analytics"])
                                with tab1:
                                    st.dataframe(df)
                                with tab2:
                                    st.image(pie.content)
                                if st.button("Refrech", width='stretch'):
                                    st.rerun()
                            except Exception as e:
                                st.error(f"Backend Error {e}")
                            
                        elif res.status_code == 404:
                            st.error(f"No Result For This Period Of Time")
                except Exception as e:
                    st.error(f"Backend Error {e}")
                    
        if st.session_state.page == "Settings":
            st.image("front.png", width=160)
            if "verify" not in st.session_state:
                st.session_state.verify = None
            if not st.session_state.verify:
                pwd = st.text_input("Password", placeholder="Please Enter Your Password To Verify Your Identity", type="password")
                if st.button("Verify", width='stretch'):
                    try:
                        query = {"pwd": pwd}
                        res = requests.post(f"{API_URL_AUTH}/verify", headers=st.session_state.headers, params= query)
                        if res.status_code == 200:
                            st.session_state.verify = True
                            st.rerun()
                        elif res.status_code == 401:
                            st.error("Wrong Password")
                        
                    except Exception as e:
                        st.error(f"Backend Error: {e}")
            else:
                tab1, tab2, tab3 = st.tabs(["Change Password", "Change Phone Number", "Add/Change Emergency Phone"])
                with tab1:
                    with st.form("password"):
                        pwd1 = st.text_input("Password*", key='pwd1', type='password')
                        pwd2 = st.text_input("Confrim Password*", key='pwd2', type='password')
                        submit = st.form_submit_button("Submit", width='stretch', key='1')

                    if submit:
                        if not pwd1 or not pwd2:
                            st.error("Please fill out all fields marked with an asterisk (*)")
                        elif pwd1 != pwd2:
                            st.error("Passwords Don't Match")
                    
                        else:
                            if not check_pwd(pwd1):
                                st.error("Verification Failed: Your password must be at least 10 characters long and include a mix of uppercase letters, lowercase letters, and numbers.")                                  
                                
                            else:
                                payload = {"password": pwd1}
                                try:
                                    res = requests.patch(API_URL, headers=st.session_state.headers, json=payload)
                                    if res.status_code == 200:
                                        st.success("Password Updated!")
                                except Exception as e:
                                    st.error(f"Backend Error: {e}")
                    st.divider()
                    if st.button("Close Settings", key='close 1', width='stretch'):
                        st.session_state.verify = None
                        st.rerun()
                with tab2:
                    with st.form("phone"):
                        p1 = st.text_input("Phone Number*", key='p1')
                        p2 = st.text_input("Phone Number*", key='p2')
                        submit = st.form_submit_button("Submit", width='stretch', key='2')
                    if submit:
                        if not p1 or not p2:
                            st.error("Please fill out all fields marked with an asterisk (*)")

                        elif p1 != p2:
                            st.error("Numbers Don't Match")
                        
                        else:
                            payload = {"phone": p1}
                            try:
                                res = requests.patch(API_URL, headers=st.session_state.headers, json=payload)
                                if res.status_code == 200:
                                    st.success("Phone Updated!")
                                elif res.status_code == 422:
                                    st.error("Please Enter a Valid Phone NUmber, e. g +2126XXXXXXXX")
                            except Exception as e:
                                st.error(f"Backend Error: {e}")
                    st.divider()
                    if st.button("Close Settings", key='close 2', width='stretch'):
                        st.session_state.verify = None
                        st.rerun()
                with tab3:
                    with st.form("emer phone"):
                        ep1 = st.text_input("Emergency Phone", key='ep1')
                        ep2 = st.text_input("Emergency Phone", key='ep2')
                        submit = st.form_submit_button("Submit", key='3', width='stretch')
                    if submit:
                        if not ep1 or not ep2:
                            st.error("Please fill out all fields marked with an asterisk (*)")

                        elif ep1 != ep2:
                            st.error("Numbers Don't Match")
                        else:
                            payload = {"emergency_phone": ep1}
                            try:
                                res = requests.patch(API_URL, headers=st.session_state.headers, json=payload)
                                if res.status_code == 200:
                                    st.success("Emergency Phone Updated!")
                                elif res.status_code == 422:
                                    st.error("Please Enter a Valid Phone NUmber, e. g +2126XXXXXXXX")
                            except Exception as e:
                                st.error(f"Backend Error: {e}") 
                    st.divider()
                    if st.button("Close Settings", key='close 3', width='stretch'):
                        st.session_state.verify = None
                        st.rerun()
                        
        if st.session_state.page == "Contract":
            st.image("front.png", width=160)
            if st.button("View Contract", width='stretch'):
                st.divider()
                try:
                    res = requests.get(f"{API_URL}/contracts/{st.session_state.user["id"]}", headers = st.session_state.headers)
                    if res.status_code == 200:
                        res = res.json()
                        file_path = os.path.join(root, res)
                        with open(file_path, "rb") as f:
                            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)

                    elif res.status_code == 404:
                        st.error("Your Contract Was Not Uploaded")
                except Exception as e:
                    st.error(f"Backend Error {e}")
    if st.session_state.user["role"] == "Manager":
        if "page" not in st.session_state:
            st.session_state.page = "Home"

        st.sidebar.image("front.png")
        st.sidebar.title("")
        
        if st.sidebar.button("Home", width='stretch'):
            st.session_state.page = "Home"
        if st.sidebar.button("Employees", width='stretch'):
            st.session_state.page = "Employees"
        if st.sidebar.button("Leave Requests", width='stretch'):
            st.session_state.page = "Leave Requests"
        if st.sidebar.button("Attendance", width='stretch'):
            st.session_state.page = "Attendance"
        if st.sidebar.button("Settings", width='stretch'):
            st.session_state.page = "Settings"
        if st.sidebar.button("Contract", width='stretch'):
            st.session_state.page = "Contract"
        if st.sidebar.button("🚪 Logout", width='stretch'):
            st.session_state.clear()
            st.rerun()

        if st.session_state.page == "Home":

            if "info" not in st.session_state:
                st.session_state.info = None
    
            try:
                info = requests.get(f"{API_URL}/{st.session_state.user['id']}", headers=st.session_state.headers)
                if info.status_code == 200:
                    if not st.session_state.info:
                        st.session_state.info = Employee_s(**info.json())
            except Exception as e:
                st.error(f"Backend Error {e}")
    
            if st.session_state.info:
    
                st.image("front.png", width=160)
    
                col1, col2 = st.columns([1, 3])
    
                with col1:
                    img = os.path.join(root, st.session_state.info.photo) if st.session_state.info.photo else "default.png"
                    st.image(img, width=120)
    
                with col2:
                    st.markdown(f"""
                    ## Welcome {st.session_state.info.first_name} {st.session_state.info.last_name}
                    **Role:** {st.session_state.info.role.value}
                    """)
    
                st.markdown("---")
    
                col1, col2 = st.columns(2)
    
                
                cmp_name = requests.get(API_URL_COMP, headers=st.session_state.headers)
                if cmp_name.status_code == 200:
                    st.session_state.cmp_name = cmp_name.json()
                elif cmp_name.status_code == 404:
                    st.error("Something Went Wrong")
                with col1:
                    st.info(f"📧 Email: {st.session_state.info.email}")
                    st.info(f"📱 Phone: {st.session_state.info.phone}")
    
                with col2:
                    st.info(f"🏢 Department: {st.session_state.info.department}")
                    st.info(f"Company: {st.session_state.cmp_name}")
                    
        if st.session_state.page == "Employees":
            st.image("front.png", width=160)
            try:
                slug = requests.get(f"{API_URL_COMP}/slug", headers = st.session_state.headers)
                if slug.status_code == 200:
                    slug = slug.json()
                    st.markdown(f":red['Your Company Slug Is {slug}, Give it To The New Employees Because They Gonna Need It To Login']")
                else:
                    st.error("Something Went Wrong")
            except Exception as e:
                st.error(f"Backend Error: {e}")
                
            add, listall, showprofile = st.tabs([
                "Add Employee", "List Employees", "Employee Profile"
            ])
        
            with add:
                
                with st.form("add_employee_form"):
                    col1, col2 = st.columns(2)
                    l = []
                    with col1:
                        first_name = st.text_input("First Name *")
                        l.append(first_name)
                        middle_name = st.text_input("Middle Name (Optional)")
                        last_name = st.text_input("Last Name *")
                        l.append(last_name)
                        gender = st.selectbox("Gender *", ["Male", "Female"])
                        l.append(gender)
                        dob = st.date_input("Date of Birth *", min_value=date(1900, 1, 1))
                        l.append(dob)
                        phone = st.text_input("Phone Number *")
                        l.append(phone)
                        email = st.text_input("Email *")
                        l.append(email)
                        address = st.text_area("Address *")
                        l.append(address)
                        photo = st.file_uploader("Upload Photo", type=["png", "jpg", "jpeg"])
                        role = st.selectbox("Role *", options=["Manager", "Employee"])
                        l.append(role)
                    with col2:
                        department = st.text_input("Department *")
                        l.append(department)
                        job_name = st.text_input("Job Title / Role")
                        supervisor = st.text_input("Supervisor")
                        employment_type = st.selectbox("Employment Type *", ["Full-time", "Part-time"])
                        l.append(employment_type)
                        start_date = st.date_input("Start Date *")
                        l.append(start_date)
                        status = st.selectbox("Status *", ["Active", "On Leave", "Inactive", "Resigned"])
                        l.append(status)
                        contract_type = st.selectbox("Contract Type *", ["Employee", "Temporary", "Intern"])
                        l.append(contract_type)
                        contract_pdf = st.file_uploader("Upload Contract PDF", type=["pdf"])
                        emergency_phone = st.text_input("Emergency Contact Phone (Optional)")
                        pwd1 = st.text_input("Password *", type="password", key="pwd1")
                        l.append(pwd1)
                        pwd2 = st.text_input("Password *", type="password", key="pwd2")
                        l.append(pwd2)
                    submit = st.form_submit_button("Add Employee")
                
                    if submit:
                        if not all(l):
                            st.error("Please fill out all fields marked with an asterisk (*)")
                        elif pwd1 != pwd2:
                            st.error("Passwords Don't match")
                        elif not check_pwd(pwd1):
                            st.error("Verification Failed: Your password must be at least 10 characters long and include a mix of uppercase letters, lowercase letters, and numbers.") 
                        else:
                            emp_payload = {
                                "first_name": first_name.title(),
                                "middle_name": middle_name.title() if middle_name else None,
                                "last_name": last_name.title(),
                                "gender": gender, 
                                "dob": str(dob),
                                "phone": phone,
                                "email": email,
                                "address": address,
                                "photo": save_upload(photo, "photos"), 
                                "department": department,
                                "role": role,
                                "job_name": job_name,
                                "password": pwd1,
                                "supervisor": supervisor if supervisor else None,
                                "employment_type": employment_type,       
                                "start_date": str(start_date),
                                "status": status,
                                "contract_type": contract_type,
                                "contract_pdf": save_upload(contract_pdf, "contracts"),
                                "emergency_phone": emergency_phone if emergency_phone else None,
                                "company_id": st.session_state.user["company_id"]
                            }
                            try:
                                response = requests.post(API_URL, json=emp_payload, headers=st.session_state.headers)
                                if response.status_code == 200:
                                    st.success("Employee Added Successfully!")
                                    st.balloons()
                                    st.toast("Success!", icon="✅")
                                elif response.status_code == 422:
                                    st.error("Make Sure You Provide a Valid Email And Your Phone have country code: e.g +2126XXXXXXXX")
                                elif response.status_code == 409:
                                    st.error("Email Already Used")
                            except Exception as e:
                                st.error(f"Error: {e}")
        
            with listall:
                try:
                    response = requests.get(f"{API_URL}/dataframe", headers=st.session_state.headers)
                    if response.status_code == 200:
                        st.dataframe(response.json())
                    elif response.status_code == 404:
                        st.warning("No employees found in the database.")
        
                except Exception as e:
                    st.error(f"Error: {e}")
            
            with showprofile:
                try: 
                    result = requests.get(API_URL, headers=st.session_state.headers)
                    if result.status_code == 200:
                        data = result.json()
                        to_show = st.selectbox(
                            "Select Employee",
                            options=list(data.keys()), 
                            format_func=lambda x: data[x],
                            key="prof_select"
                        )
                        
                        if st.button("Show Profile", width='stretch', key="prof_btn"):
                            emp_api = requests.get(f"{API_URL}/{to_show}", headers=st.session_state.headers)
                            if emp_api.status_code == 200:
                                root = os.getenv("UPLOADS_ROOT", "/myapp/uploads")
                                emp = Employee_s(**emp_api.json())
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
        if st.session_state.page == "Leave Requests":
            
            def display_pdf(base64_pdf):
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            
            res = requests.get(f"{API_URL_REQ}/AdMan", headers=st.session_state.headers)
            requests_list = res.json()
            
            if not requests_list:
                st.info("No pending requests found.")
            else:
                for req in requests_list:
                    st.subheader(f"Request from: {req['first_name']} {req['last_name']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Employee ID:** {req['emp_id']}")
                        st.write(f"**Request Date:** {req['date']}")
                        st.write(f"**Reason:** {req['reason']}")
                        
                    with col2:
                        st.write(f"**Start Date:** {req['start_date']}")
                        st.write(f"**End Date:** {req['end_date']}")
            
                    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 2])
                    
                    with btn_col1:
                        if st.button("Accept", key=f"acc_{req['id']}"):
                            try:
                                payload = {"id": req['id'], "status": "Approved"}
                                requests.patch(f"{API_URL_REQ}/AdMan", params=payload, headers=st.session_state.headers)
                                st.rerun()
                            except Exception as e:
                                st.error(f"backend error: {e}")
            
                    with btn_col2:
                        if st.button("Reject", key=f"rej_{req['id']}"):
                            try:
                                payload = {"id": req['id'], "status": "Rejected"}
                                requests.patch(f"{API_URL_REQ}/AdMan", params=payload, headers=st.session_state.headers)
                                st.rerun()
                            except Exception as e:
                                st.error(f"backend error: {e}")
            
                    if req.get('doc'):
                        if st.session_state.get(f"show_{req['id']}", False):
                            if st.button("Close Preview", key=f"close_{req['id']}"):
                                st.session_state[f"show_{req['id']}"] = False
                                st.rerun()
                            pdf_path = os.path.join(root, req['doc'])
                            with open(pdf_path, "rb") as f:
                                pdf_b64 = base64.b64encode(f.read()).decode('utf-8')
                            display_pdf(pdf_b64)
                        else:
                            if st.button("📄 View Document", key=f"view_{req['id']}"):
                                st.session_state[f"show_{req['id']}"] = True
                                st.rerun()
                    else:
                        st.warning("No document attached.")
            
                    st.divider()
        if st.session_state.page == "Settings":
            st.image("front.png", width=160)
            if "verify" not in st.session_state:
                st.session_state.verify = None
            if not st.session_state.verify:
                pwd = st.text_input("Password", placeholder="Please Enter Your Password To Verify Your Identity", type="password")
                if st.button("Verify", width='stretch'):
                    try:
                        query = {"pwd": pwd}
                        res = requests.post(f"{API_URL_AUTH}/verify", headers=st.session_state.headers, params= query)
                        if res.status_code == 200:
                            st.session_state.verify = True
                            st.rerun()
                        elif res.status_code == 401:
                            st.error("Wrong Password")
                        
                    except Exception as e:
                        st.error(f"Backend Error: {e}")
            else:
                tab1, tab2, tab3 = st.tabs(["Change Password", "Change Phone Number", "Add/Change Emergency Phone"])
                with tab1:
                    with st.form("password"):
                        pwd1 = st.text_input("Password*", key='pwd1', type='password')
                        pwd2 = st.text_input("Confrim Password*", key='pwd2', type='password')
                        submit = st.form_submit_button("Submit", width='stretch', key='1')

                    if submit:
                        if not pwd1 or not pwd2:
                            st.error("Please fill out all fields marked with an asterisk (*)")
                        elif pwd1 != pwd2:
                            st.error("Passwords Don't Match")
                    
                        else:
                            if not check_pwd(pwd1):
                                st.error("Verification Failed: Your password must be at least 10 characters long and include a mix of uppercase letters, lowercase letters, and numbers.")                                  
                                
                            else:
                                payload = {"password": pwd1}
                                try:
                                    res = requests.patch(API_URL, headers=st.session_state.headers, json=payload)
                                    if res.status_code == 200:
                                        st.success("Password Updated!")
                                except Exception as e:
                                    st.error(f"Backend Error: {e}")
                    st.divider()
                    if st.button("Close Settings", key='close 1', width='stretch'):
                        st.session_state.verify = None
                        st.rerun()
                with tab2:
                    with st.form("phone"):
                        p1 = st.text_input("Phone Number*", key='p1')
                        p2 = st.text_input("Phone Number*", key='p2')
                        submit = st.form_submit_button("Submit", width='stretch', key='2')
                    if submit:
                        if not p1 or not p2:
                            st.error("Please fill out all fields marked with an asterisk (*)")

                        elif p1 != p2:
                            st.error("Numbers Don't Match")
                        
                        else:
                            payload = {"phone": p1}
                            try:
                                res = requests.patch(API_URL, headers=st.session_state.headers, json=payload)
                                if res.status_code == 200:
                                    st.success("Phone Updated!")
                                elif res.status_code == 422:
                                    st.error("Please Enter a Valid Phone NUmber, e. g +2126XXXXXXXX")
                            except Exception as e:
                                st.error(f"Backend Error: {e}")
                    st.divider()
                    if st.button("Close Settings", key='close 2', width='stretch'):
                        st.session_state.verify = None
                        st.rerun()
                with tab3:
                    with st.form("emer phone"):
                        ep1 = st.text_input("Emergency Phone", key='ep1')
                        ep2 = st.text_input("Emergency Phone", key='ep2')
                        submit = st.form_submit_button("Submit", key='3', width='stretch')
                    if submit:
                        if not ep1 or not ep2:
                            st.error("Please fill out all fields marked with an asterisk (*)")

                        elif ep1 != ep2:
                            st.error("Numbers Don't Match")
                        else:
                            payload = {"emergency_phone": ep1}
                            try:
                                res = requests.patch(API_URL, headers=st.session_state.headers, json=payload)
                                if res.status_code == 200:
                                    st.success("Emergency Phone Updated!")
                                elif res.status_code == 422:
                                    st.error("Please Enter a Valid Phone NUmber, e. g +2126XXXXXXXX")
                            except Exception as e:
                                st.error(f"Backend Error: {e}") 
                    st.divider()
                    if st.button("Close Settings", key='close 3', width='stretch'):
                        st.session_state.verify = None
                        st.rerun()
        if st.session_state.page == "Contract":
            st.image("front.png", width=160)
            if st.button("View Contract", width='stretch'):
                st.divider()
                try:
                    res = requests.get(f"{API_URL}/contracts/{st.session_state.user["id"]}", headers = st.session_state.headers)
                    if res.status_code == 200:
                        res = res.json()
                        file_path = os.path.join(root, res)
                        with open(file_path, "rb") as f:
                            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)

                    elif res.status_code == 404:
                        st.error("Your Contract Was Not Uploaded")
                except Exception as e:
                    st.error(f"Backend Error {e}")

        if st.session_state.page == "Attendance":
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
                    if not st.session_state.check:
                        if st.button("Initialize Today's Attendance", width='stretch'):
                            check = requests.get(f"{API_URL_att}/date", params=query, headers=st.session_state.headers)
                            if check.status_code == 409:
                                st.warning("Attendance for today has already been recorded. To prevent fraud and ensure data integrity, the system is locked for new entries until tomorrow.")
                                time.sleep(6)
                                st.rerun()
                            elif check.status_code == 200:
                                st.session_state.check = True
                except Exception as e:
                    st.error(f"Backend unavailable: {e}")
                
                if st.session_state.check:
                    if not st.session_state.emps:
                        try:
                            res = requests.get(API_URL_att, headers=st.session_state.headers)
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
                                    res = requests.post(API_URL_att, json=payload, headers=st.session_state.headers)
                                    if res.status_code == 200:
                                        st.success("Attendance recorded successfully.")
                                        st.session_state.emps = {}
                                        st.session_state.check = False
                                        time.sleep(6)
                                        st.rerun()
                                    else:
                                        st.error(f"Error: {res.text}")
                                except Exception as e:
                                    st.error(f"Error: {e}")
            with records:
                radio = st.radio("View Scope", options=["Single Employee", "All Employees"], horizontal=True, key="records")
                if radio == "Single Employee":
                    try: 
                        result = requests.get(API_URL, headers = st.session_state.headers)
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
                            with col1:
                                start = st.date_input("Start Date", min_value=date(2010, 1, 1), value=None, key="start")
                            with col2:
                                end = st.date_input("End Date", min_value=date(2010, 1, 1), value=None, key="end")
                            if st.button("Show Records", width='stretch'):
                                payload = {}
                                if start:
                                    payload["start"] = str(start)
                                if end:
                                    payload["end"] = str(end)
                                try:
                                    record = requests.get(f"{API_URL_att}/records/{id}", params=payload, headers=st.session_state.headers)
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
                    with col1:
                        start = st.date_input("Start Date", min_value=date(2010, 1, 1), value=None, key="start")
                    with col2:
                        end = st.date_input("End Date", min_value=date(2010, 1, 1), value=None, key="end")
                    if st.button("Show Records", width='stretch'):
                        payload = {}
                        if start:
                            payload["start"] = str(start)
                        if end:
                            payload["end"] = str(end)
                        try:
                            record = requests.get(f"{API_URL_att}/records", params=payload, headers=st.session_state.headers)
                        except Exception as e:
                            st.error(f"Error: {e}")
                        
                        if record.status_code == 200:
                            pre_df = record.json()
                            st.dataframe(pre_df)
                        elif record.status_code == 404:
                            st.warning("No Records For This Time Period")
                        if st.button("Refresh", key="refresh", width='stretch'):
                            st.rerun()
            with analytics:
                radio = st.radio("View Scope", options=["Single Employee", "All Employees"], horizontal=True, key="analytics")
                if radio == "Single Employee":               
                    try: 
                        result = requests.get(API_URL, headers=st.session_state.headers)
                        if result.status_code == 200:
                            st.session_state.selectbox = result.json()
                            st.selectbox(
                                "Select Employee",
                                options=list(st.session_state.selectbox.keys()), 
                                format_func=lambda x: st.session_state.selectbox[x],
                                key="id"
                            )
                            col1, col2 = st.columns(2)
                            st.markdown("Enter Start and End Date of the Records, To Show All Time Records Leave Them Empty")
                            with col1:
                                st.date_input("Start Date", min_value=date(2010, 1, 1), value=None, key="start_e")
                            with col2:
                                st.date_input("Start Date", min_value=date(2010, 1, 1), value=None, key="end_e")
                            if st.button("Show Analytics"):
                                payload = {}
                                if st.session_state.start_e:
                                    payload["start"] = st.session_state.start_e
                                if st.session_state.end_e:
                                    payload["end"] = st.session_state.end_e
                                try:
                                    record = requests.get(f"{API_URL_att}/analytics/piechart/{st.session_state.id}", params=payload, headers=st.session_state.headers)
                                except Exception as e:
                                    st.error(f"Error: {e}")
                                if record.status_code == 200:
                                    st.image(record.content)
                                          
                                elif record.status_code == 404:
                                    st.warning("No Records For This Employee In This Time Period")
                                st.divider()
                                if st.button("Refresh", key="refresh", width='stretch'):
                                    st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                if radio == "All Employees":
        
                    
                    st.markdown("Enter Start and End Date of the Records, To Show All Time Records Leave Them Empty")
                    tab1, tab2 = st.tabs(["Overview", "Trends"])
                    with tab1:
                        st.markdown("Enter Start and End Date of the Records, To Show All Time Records Leave Them Empty")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.date_input("Start Date", min_value=date(2010, 1, 1), value=None, key="start_o")
                        with col2:
                            st.date_input("Start Date", min_value=date(2010, 1, 1), value=None, key="end_o")
                        payload = {}
                        if st.session_state.start_o:
                            payload["start"] = st.session_state.start_o
                        if st.session_state.end_o:
                            payload["end"] = st.session_state.end_o
                        if st.button("Show Overview"):
                            try:
                                record = requests.get(f"{API_URL_att}/analytics/piechart", params=payload, headers=st.session_state.headers)
                            except Exception as e:
                                st.error(f"Error: {e}")
                            if record.status_code == 200:
                                st.image(record.content)
                            
                    with tab2:
                        st.markdown("Enter Start and End Date of the Records, To Show All Time Records Leave Them Empty")
                        col1, col2 = st.columns(2)
                        st.selectbox(
                            "Chose Which Status To Plot Over Time Or Chose All To Plot All Status",
                            options=["Remote", "Vacation", "Sick", "Absent", "Present", "All"],
                            key="status",
                        )
                        with col1:
                            st.date_input("Start Date", min_value=date(2010, 1, 1), value=None, key="start_t")
                        with col2:
                            st.date_input("Start Date", min_value=date(2010, 1, 1), value=None, key="end_t")
                        payload = {"status": st.session_state.status}
                        if st.session_state.start_t:
                            payload["start"] = st.session_state.start_t
                        if st.session_state.end_t:
                            payload["end"] = st.session_state.end_t
                        if st.button("Show Trend", width='stretch'):
                            try:
                                record = requests.get(f"{API_URL_att}/analytics/plots", params=payload, headers=st.session_state.headers)
                            except Exception as e:
                                st.error(f"Error: {e}")
                            if record.status_code == 200:
                                st.image(record.content)
                        
    if st.session_state.user["role"] == "Admin":
        if "page" not in st.session_state:
            st.session_state.page = "Home"

        st.sidebar.image("front.png")
        st.sidebar.title("")
        
        if st.sidebar.button("Home", width='stretch'):
            st.session_state.page = "Home"
        if st.sidebar.button("Employees", width='stretch'):
            st.session_state.page = "Employees"
        if st.sidebar.button("Settings", width='stretch'):
            st.session_state.page = "Settings"
        if st.sidebar.button("🚪 Logout", width='stretch'):
            st.session_state.clear()
            st.rerun()

        if st.session_state.page == "Home":
            st.image("front.png", width=160)
            try:
                cmp_name = requests.get(API_URL_COMP, headers = st.session_state.headers)
                slug = requests.get(f"{API_URL_COMP}/slug", headers = st.session_state.headers)
                if cmp_name.status_code == 200 and slug.status_code == 200:
                    cmp_name = cmp_name.json()
                    slug = slug.json()
                else:
                    st.error("Something Went Wrong")
                    st.stop()
            except Exception as e:
                st.error(f"Backend Error {e}")
                
            st.markdown(f"""
                <div style="text-align: center; padding: 20px;">
                    <h1 style="color: #007bff; margin-bottom: 0;">Welcome to the Admin Panel</h1>
                    <h3 style="color: #6c757d; margin-top: 5px;">
                        for {cmp_name} (ID: {st.session_state.user["company_id"]})
                    </h3>
                    <p style="color: #007bff; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">
                        Your Company Slug IS <em><b>{slug}</b></em>
                    </p>
                </div>
            """, unsafe_allow_html=True)

            st.divider()
        if st.session_state.page == "Employees":
            st.image("front.png", width=160)
            try:
                slug = requests.get(f"{API_URL_COMP}/slug", headers = st.session_state.headers)
                if slug.status_code == 200:
                    slug = slug.json()
                    st.markdown(f":red['Your Company Slug Is {slug}, Give it To The New Employees Because They Gonna Need It To Login']")
                else:
                    st.error("Something Went Wrong")
            except Exception as e:
                st.error(f"Backend Error: {e}")
                
            
            add, delete = st.tabs(["Add Employee", "Delete Employee"])
            
            with add:
                
                with st.form("add_employee_form"):
                    col1, col2 = st.columns(2)
                    l = []
                    with col1:
                        first_name = st.text_input("First Name *")
                        l.append(first_name)
                        middle_name = st.text_input("Middle Name (Optional)")
                        last_name = st.text_input("Last Name *")
                        l.append(last_name)
                        gender = st.selectbox("Gender *", ["Male", "Female"])
                        l.append(gender)
                        dob = st.date_input("Date of Birth *", min_value=date(1900, 1, 1))
                        l.append(dob)
                        phone = st.text_input("Phone Number *")
                        l.append(phone)
                        email = st.text_input("Email *")
                        l.append(email)
                        address = st.text_area("Address *")
                        l.append(address)
                        photo = st.file_uploader("Upload Photo", type=["png", "jpg", "jpeg"])
                        role = st.selectbox("Role *", options=["Manager", "Employee"])
                        l.append(role)
                    with col2:
                        department = st.text_input("Department *")
                        l.append(department)
                        job_name = st.text_input("Job Title / Role")
                        supervisor = st.text_input("Supervisor")
                        employment_type = st.selectbox("Employment Type *", ["Full-time", "Part-time"])
                        l.append(employment_type)
                        start_date = st.date_input("Start Date *")
                        l.append(start_date)
                        status = st.selectbox("Status *", ["Active", "On Leave", "Inactive", "Resigned"])
                        l.append(status)
                        contract_type = st.selectbox("Contract Type *", ["Employee", "Temporary", "Intern"])
                        l.append(contract_type)
                        contract_pdf = st.file_uploader("Upload Contract PDF", type=["pdf"])
                        emergency_phone = st.text_input("Emergency Contact Phone (Optional)")
                        pwd1 = st.text_input("Password *", type="password", key="pwd1")
                        l.append(pwd1)
                        pwd2 = st.text_input("Password *", type="password", key="pwd2")
                        l.append(pwd2)
                    submit = st.form_submit_button("Add Employee")
                
                    if submit:
                        if not all(l):
                            st.error("Please fill out all fields marked with an asterisk (*)")
                        elif pwd1 != pwd2:
                            st.error("Passwords Don't match")
                        elif not check_pwd(pwd1):
                            st.error("Verification Failed: Your password must be at least 10 characters long and include a mix of uppercase letters, lowercase letters, and numbers.") 
                        else:
                            emp_payload = {
                                "first_name": first_name.title(),
                                "middle_name": middle_name.title() if middle_name else None,
                                "last_name": last_name.title(),
                                "gender": gender, 
                                "dob": str(dob),
                                "phone": phone,
                                "email": email,
                                "address": address,
                                "photo": save_upload(photo, "photos"), 
                                "department": department,
                                "role": role,
                                "job_name": job_name,
                                "password": pwd1,
                                "supervisor": supervisor if supervisor else None,
                                "employment_type": employment_type,       
                                "start_date": str(start_date),
                                "status": status,
                                "contract_type": contract_type,
                                "contract_pdf": save_upload(contract_pdf, "contracts"),
                                "emergency_phone": emergency_phone if emergency_phone else None,
                                "company_id": st.session_state.user["company_id"]
                            }
                            try:
                                response = requests.post(API_URL, json=emp_payload, headers=st.session_state.headers)
                                if response.status_code == 200:
                                    st.success("Employee Added Successfully!")
                                    st.balloons()
                                    st.toast("Success!", icon="✅")
                                elif response.status_code == 422:
                                    st.error("Make Sure You Provide a Valid Email And Your Phone have country code: e.g +2126XXXXXXXX")
                                elif response.status_code == 409:
                                    st.error("Email Already Used")
                            except Exception as e:
                                st.error(f"Error: {e}")
                    
            with delete:

                try: 
                    result = requests.get(API_URL, headers=st.session_state.headers)
                    if result.status_code == 200:
                        data = result.json()
                        to_delete = st.selectbox(
                            "Select Employee",
                            options=list(data.keys()), 
                            format_func=lambda x: data[x],
                            key="del_select"
                        )
                        if st.button("Confirm Deletion", use_container_width=True, key="del_confirm"):
                            deleted = requests.delete(f"{API_URL}/{to_delete}", headers=st.session_state.headers)
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
        if st.session_state.page == "Settings":
            st.image("front.png", width=160)
            if "verify" not in st.session_state:
                st.session_state.verify = None
            if not st.session_state.verify:
                pwd = st.text_input("Password", placeholder="Please Enter Your Password To Verify Your Identity", type="password")
                if st.button("Verify", width='stretch'):
                    try:
                        query = {"pwd": pwd}
                        res = requests.post(f"{API_URL_AUTH}/verify/admin", headers=st.session_state.headers, params= query)
                        if res.status_code == 200:
                            st.session_state.verify = True
                            st.rerun()
                        elif res.status_code == 401:
                            st.error("Wrong Password")
                        
                    except Exception as e:
                        st.error(f"Backend Error: {e}")
            else:
                
                
                with st.form("password"):
                    pwd1 = st.text_input("Password*", key='pwd1', type='password')
                    pwd2 = st.text_input("Confrim Password*", key='pwd2', type='password')
                    submit = st.form_submit_button("Submit", width='stretch', key='1')

                if submit:
                    if not pwd1 or not pwd2:
                        st.error("Please fill out all fields marked with an asterisk (*)")
                    elif pwd1 != pwd2:
                        st.error("Passwords Don't Match")
                
                    else:
                        if not check_pwd(pwd1):
                            st.error("Verification Failed: Your password must be at least 10 characters long and include a mix of uppercase letters, lowercase letters, and numbers.")                                  
                            
                        else:
                            payload = {"password": pwd1}
                            try:
                                res = requests.patch(API_URL_COMP, headers=st.session_state.headers, params=payload)
                                if res.status_code == 200:
                                    st.success("Password Updated!")
                            except Exception as e:
                                st.error(f"Backend Error: {e}")
                st.divider()
                if st.button("Close Settings", key='close 1', width='stretch'):
                    st.session_state.verify = None
                    st.rerun()
