import streamlit as st

st.title("AI Road Damage Detection System")

st.markdown(
    """
### Welcome

This application helps citizens detect and report road damages using Artificial Intelligence.

---

### Features

✅ Detect road damages using YOLO

✅ View annotated road images

✅ Submit reports

✅ Store reports in MongoDB

✅ View all reported damages

---
"""
)

col1, col2, col3 = st.columns([1,2,1])

with col2:
    if st.button("🚀 Get Started", use_container_width=True):
        st.switch_page("ui/pages/upload.py")