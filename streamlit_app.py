from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="StreetScan",
    page_icon=Path("ui/assets/favicon.ico"),
    layout="wide",
    initial_sidebar_state="expanded",
)

css_file = Path(__file__).parent / "ui" / "styles" / "style.css"

if css_file.exists():
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )

navigation = st.navigation(
    [
        st.Page(
            "ui/pages/home.py",
            title="Home",
        ),
        st.Page(
            "ui/pages/upload.py",
            title="Upload",
        ),
        st.Page(
            "ui/pages/reports.py",
            title="Reports",
        ),
    ]
)

navigation.run()