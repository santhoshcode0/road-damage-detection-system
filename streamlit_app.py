import streamlit as st

st.set_page_config(
    page_title="Road Damage Detection System",
    layout="wide",
    initial_sidebar_state="expanded"
)

navigation = st.navigation(
    [
        st.Page("ui/pages/home.py", title="Home"),
        st.Page("ui/pages/upload.py", title="Upload"),
        st.Page("ui/pages/reports.py", title="Reports"),
    ]
)

navigation.run()