import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

st.title("Utree Vault - Test Frontend")

# Show options only if not logged in
if not st.session_state.logged_in:
    option = st.radio("Choose an action:", ["Create Company Account", "Login"])

    # -------- Create Company --------
    if option == "Create Company Account":
        st.subheader("Create Company Account")
        with st.form("create_company_form"):
            company_name = st.text_input("Company Name")
            admin_name = st.text_input("Admin Name")
            admin_email = st.text_input("Admin Email")
            admin_password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Create Company")
            if submitted:
                # Fake API call
                st.write("Calling API to create company...")
                st.session_state.logged_in = True
                st.session_state.user_data = {
                    "role": "admin",
                    "company": company_name,
                    "name": admin_name
                }
                st.success("Company created! Logged in as Admin.")

    # -------- Login --------
    elif option == "Login":
        st.subheader("Login")
        role = st.selectbox("Select your role:", ["Employee", "Manager", "Admin"])
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login = st.form_submit_button("Login")
            if login:
                st.write(f"Logging in as {role}...")
                st.session_state.logged_in = True
                st.session_state.user_data = {
                    "role": role.lower(),
                    "email": email
                }
                st.success(f"Logged in as {role}")

if st.session_state.logged_in:
    st.subheader(f"Welcome, {st.session_state.user_data.get('role', '').capitalize()}!")
    st.write(st.session_state.user_data)
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_data = {}
        st.experimental_rerun()