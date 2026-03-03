import streamlit as st

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
    add, delete, update, listall, showprofile = st.tabs(["Add Employee", "Delete Employee", "Update Employee", "List Employees", "Employee Profile"])
    with add:
        with st.form("add employee"):
            col1, col2 = st.columns(2)

            with col1:
                first_name = st.text_input("First Name")
                middle_name = st.text_input("Middle Name (Optional)")
                last_name = st.text_input("Last Name")
                gender = st.selectbox("Gender", ["Male", "Female"])
                dob = st.date_input("Date of Birth")
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

            submitted = st.form_submit_button("Add Employee")