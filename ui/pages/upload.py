import sys
import hashlib
from pathlib import Path
from collections import Counter

import streamlit as st
from streamlit_geolocation import streamlit_geolocation

if "upload_key" not in st.session_state:
    st.session_state.upload_key = 0

# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]

SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(
        0,
        str(SRC_PATH)
    )


# --------------------------------------------------
# Imports
# --------------------------------------------------

from config import UPLOAD_FOLDER

from core.pipeline import Pipeline

from core.database import Database

from core.report_builder import ReportBuilder

from core.pdf_generator import generate_pdf


# --------------------------------------------------
# Page header
# --------------------------------------------------

st.title(
    "Road Damage Inspection"
)

st.caption(
    "Upload a road image and let StreetScan analyze "
    "visible surface damage automatically."
)

st.divider()

def reset_upload():
    st.session_state.upload_key += 1

# --------------------------------------------------
# Upload section
# --------------------------------------------------

st.subheader(
    "📷 Upload Road Image"
)

st.write(
    "Choose a clear image of the road surface. "
    "StreetScan will analyze the image and identify "
    "visible damage."
)

uploaded_file = st.file_uploader(
    "Drag & drop a road image here or click Browse",
    type=["jpg", "jpeg", "png"],
    help="Supported formats: JPG, JPEG and PNG",
    key=f"road_image_uploader_{st.session_state.upload_key}"
)


# --------------------------------------------------
# Image uploaded
# --------------------------------------------------

if uploaded_file:

    # --------------------------------------------------
    # Read uploaded file
    # --------------------------------------------------

    file_bytes = (
        uploaded_file.getvalue()
    )

    # --------------------------------------------------
    # Generate SHA-256 image hash
    # --------------------------------------------------

    image_hash = hashlib.sha256(
        file_bytes
    ).hexdigest()


    # --------------------------------------------------
    # Connect to database
    # --------------------------------------------------

    try:

        db = Database()

    except Exception as e:

        st.error(
            "Unable to connect to the database."
        )

        st.exception(e)

        st.stop()


    # --------------------------------------------------
    # Check for duplicate image
    # --------------------------------------------------

    existing_report = (
        db.get_report_by_image_hash(
            image_hash
        )
    )


    if existing_report:

        existing_report_number = (
            existing_report.get(
                "report_number",
                existing_report.get(
                    "report_id",
                    "Unknown"
                )
            )
        )

        st.warning(
            "This image has already been inspected."
        )

        st.info(
            f"A duplicate report was not created. "
            f"Existing report: "
            f"{existing_report_number}"
        )

        st.stop()


    # --------------------------------------------------
    # Save uploaded image
    # --------------------------------------------------

    UPLOAD_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    image_path = (
        UPLOAD_FOLDER /
        uploaded_file.name
    )

    with open(
        image_path,
        "wb"
    ) as f:

        f.write(
            file_bytes
        )


    st.success(
        f"Image uploaded successfully: "
        f"{uploaded_file.name}"
    )

    st.divider()


    # --------------------------------------------------
    # Image preview
    # --------------------------------------------------

    st.subheader(
        "🖼️ Image Preview"
    )

    preview_col1, preview_col2, preview_col3 = (
        st.columns(
            [1, 3, 1]
        )
    )

    with preview_col2:

        st.image(
            image_path,
            use_container_width=True
        )

    st.write("")

    # --------------------------------------------------
    # Inspection Location
    # --------------------------------------------------

    st.subheader("📍 Inspection Location")

    st.write(
        "Add the inspection location to include it in "
        "the inspection report."
    )

    location_col1, location_col2 = st.columns(
        [1, 1],
        gap="medium"
    )

    with location_col1:

        location = streamlit_geolocation()

    with location_col2:

        address = st.text_input(
            "Address (optional)",
            placeholder="e.g. Bengaluru, Karnataka"
        )
    latitude = None
    longitude = None

    if location:

        latitude = location.get(
            "latitude"
        )

        longitude = location.get(
            "longitude"
        )

        if latitude is not None and longitude is not None:

            st.success(
                f"Location captured: "
                f"{latitude:.6f}, "
                f"{longitude:.6f}"
            )

    # --------------------------------------------------
    # Analyze button
    # --------------------------------------------------

    analyze_col1, analyze_col2, analyze_col3 = (
        st.columns(
            [1, 2, 1]
        )
    )

    with analyze_col2:

        analyze_button = st.button(
            "🔍 Analyze Road Damage",
            use_container_width=True,
            type="primary"
        )


    # --------------------------------------------------
    # Run inspection
    # --------------------------------------------------

    if analyze_button:

        try:

            with st.spinner(
                "Analyzing the road image... "
                "This may take a moment."
            ):

                pipeline = Pipeline()

                result = pipeline.process_image(
                    str(image_path)
                )


        except Exception as e:

            st.error(
                "The inspection could not be completed."
            )

            st.exception(e)

            st.stop()


        st.toast(
            "Inspection completed successfully.",
            icon="✅"
        )

        st.divider()


        # --------------------------------------------------
        # Inspection results
        # --------------------------------------------------

        st.subheader(
            "🔎 Inspection Results"
        )

        original_col, result_col = (
            st.columns(
                2,
                gap="large"
            )
        )

        with original_col:

            st.markdown(
                "#### Original Image"
            )

            st.image(
                image_path,
                use_container_width=True
            )

        with result_col:

            st.markdown(
                "#### Detected Road Damage"
            )

            st.image(
                result["annotated_image"],
                use_container_width=True
            )

        st.divider()


        # --------------------------------------------------
        # Assessment
        # --------------------------------------------------

        assessment = result[
            "assessment"
        ]

        road_condition = assessment[
            "road_condition"
        ]

        risk_level = assessment[
            "risk_level"
        ]

        maintenance_priority = assessment[
            "maintenance_priority"
        ]

        repair_category = assessment[
            "repair_category"
        ]

        damage_count = result[
            "total_damages"
        ]


        # --------------------------------------------------
        # Road condition display
        # --------------------------------------------------

        if road_condition == "Good":

            status_display = "🟢 Good"

        elif road_condition == "Moderate":

            status_display = "🟡 Moderate"

        else:

            status_display = "🔴 Critical"


        # --------------------------------------------------
        # Inspection summary
        # --------------------------------------------------

        st.subheader(
            "📊 Inspection Summary"
        )

        summary_col1, summary_col2, summary_col3 = (
            st.columns(
                3,
                gap="medium"
            )
        )

        with summary_col1:

            st.metric(
                "Road Condition",
                status_display
            )

        with summary_col2:

            st.metric(
                "Damages Detected",
                damage_count
            )

        with summary_col3:

            st.metric(
                "Repair Category",
                repair_category
            )


        # --------------------------------------------------
        # Maintenance assessment
        # --------------------------------------------------

        st.subheader(
            "⚠️ Maintenance Assessment"
        )

        assessment_col1, assessment_col2 = (
            st.columns(
                2,
                gap="medium"
            )
        )

        with assessment_col1:

            st.metric(
                "Risk Level",
                risk_level
            )

        with assessment_col2:

            st.metric(
                "Maintenance Priority",
                maintenance_priority
            )


        st.divider()


        # --------------------------------------------------
        # Damage summary
        # --------------------------------------------------

        st.subheader(
            "🎯 Detected Damages"
        )

        if result["detections"]:

            damage_counts = Counter(
                d["damage_type"]
                .replace(
                    "_",
                    " "
                )
                .title()
                for d in result["detections"]
            )

            display_data = [
                {
                    "Damage Type": damage,
                    "Count": count
                }

                for damage, count
                in damage_counts.items()
            ]

            st.dataframe(
                display_data,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "No visible road damage was detected."
            )


        # --------------------------------------------------
        # AI inspection report
        # --------------------------------------------------

        st.divider()

        st.subheader(
            "📝 AI Inspection Report"
        )

        st.markdown(
            result["ai_report"]
        )


        # --------------------------------------------------
        # Save report
        # --------------------------------------------------

        try:

            report_number = (
                db.get_next_report_number()
            )

            report = ReportBuilder.build(
                detection_result=result,
                report_number=report_number,
                ai_report=result["ai_report"],
                assessment=result["assessment"],
                image_hash=image_hash,
                latitude=latitude,
                longitude=longitude,
                address=address
            )

            db.save_report(
                report
            )


        except Exception as e:

            st.error(
                "The inspection was completed, "
                "but the report could not be saved."
            )

            st.exception(e)

            st.stop()


        st.toast(
            "Report saved successfully.",
            icon="✅"
        )


        # --------------------------------------------------
        # Download PDF
        # --------------------------------------------------

        st.divider()

        st.subheader(
            "📄 Inspection Report"
        )

        st.write(
            "Your inspection has been saved. "
            "You can download the complete PDF "
            "report below."
        )

        try:

            pdf_bytes = generate_pdf(
                report
            )

            st.download_button(
                label="📄 Download Inspection Report",
                data=pdf_bytes,
                file_name=f"{report['report_number']}.pdf",
                mime="application/pdf",
                use_container_width=True,
                on_click=reset_upload
            )

        except Exception as e:

            st.error(
                "The PDF report could not be generated."
            )

            st.exception(e)


else:

    # --------------------------------------------------
    # Empty upload state
    # --------------------------------------------------

    st.info(
        "Upload a road image above to begin an inspection."
    )