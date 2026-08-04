import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from config import UPLOAD_FOLDER
from core.pipeline import Pipeline


st.title("Upload Road Image")

st.write("Upload a road image and click Detect to analyze it.")

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    image_path = UPLOAD_FOLDER / uploaded_file.name

    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(image_path, use_container_width=True)

    if st.button("Detect Damage", use_container_width=True):

        with st.spinner("Analyzing road image..."):

            pipeline = Pipeline()
            result = pipeline.process_image(str(image_path))

        st.success("Detection completed successfully.")

        st.subheader("Annotated Image")
        st.image(result["annotated_image"], use_container_width=True)

        st.subheader("Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Damages", result["total_damages"])

        with col2:
            st.metric("Processing Time", f"{result['processing_time']} sec")

        st.subheader("Detections")

        if result["detections"]:
            st.dataframe(
                result["detections"],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No damages detected.")