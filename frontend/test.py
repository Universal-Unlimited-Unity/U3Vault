import streamlit as st

def show_employee_profile(employee_data):
    # Styling for the card container
    st.markdown("""
        <style>
        .profile-card {
            border: 1px solid #e6e9ef;
            border-radius: 15px;
            padding: 20px;
            background-color: #f8f9fb;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        # Create columns: 1 for image, 2 for info, 1 for the action button
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            # Assuming employee_data['photo_url'] is a path or URL
            st.image("https://via.placeholder.com/150", width=120) 

        with col2:
            st.subheader(f"{employee_data['first_name']} {employee_data['last_name']}")
            st.caption(f"📍 {employee_data['department']} | {employee_data['role']}")
            
            # Key Info in a small grid
            info_col_a, info_col_b = st.columns(2)
            info_col_a.write(f"**ID:** {employee_data['emp_id']}")
            info_col_b.write(f"**Email:** {employee_data['email']}")

        with col3:
            st.write(" ") # Spacer
            st.write(" ")
            if st.button("📄 View Contract", key=f"btn_{employee_data['emp_id']}"):
                # This is where your backend logic kicks in
                st.info(f"Opening contract for {employee_data['last_name']}...")

    st.divider()

# --- Inside your Tabs ---
tab1, tab2 = st.tabs(["List View", "Employee Profile"])

with tab2:
    # Mock data from your JSON
    mock_employee = {
        "first_name": "Hamza",
        "last_name": "Kaddouri",
        "department": "Engineering",
        "role": "Python Developer",
        "emp_id": "U3-9921",
        "email": "h.kaddouri@fssm.ma"
    }
    
    show_employee_profile(mock_employee)