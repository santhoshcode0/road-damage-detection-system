import sys
from pathlib import Path
from collections import Counter
from datetime import datetime

import streamlit as st

# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

# --------------------------------------------------
# Imports
# --------------------------------------------------

from core.database import Database
from core.pdf_generator import generate_pdf


# --------------------------------------------------
# Page title
# --------------------------------------------------

st.title("All Reports")

st.caption(
    "View, search and manage all StreetScan road inspections."
)

st.divider()


# --------------------------------------------------
# Load reports
# --------------------------------------------------

try:
    db = Database()
    reports = db.get_all_reports()

except Exception as e:
    st.exception(e)
    st.stop()


# --------------------------------------------------
# No reports
# --------------------------------------------------

if not reports:

    st.info(
        "No inspection reports found yet. "
        "Upload a road image to generate your first report."
    )

    st.stop()


# --------------------------------------------------
# Search & filters
# --------------------------------------------------

st.subheader("🔎 Search & Filter")

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(
    [2, 1, 1, 1],
    gap="medium"
)


# --------------------------------------------------
# Search
# --------------------------------------------------

with filter_col1:

    search_query = st.text_input(
        "Search Report",
        placeholder="Search by Report ID...",
        help="Example: REP-0001"
    )


# --------------------------------------------------
# Status filter
# --------------------------------------------------

with filter_col2:

    status_filter = st.selectbox(
        "Status",
        [
            "All",
            "Pending",
            "Completed"
        ]
    )


# --------------------------------------------------
# Date filter
# --------------------------------------------------

with filter_col3:

    date_filter = st.date_input(
        "Date",
        value=None,
        format="DD/MM/YYYY",
    )


# --------------------------------------------------
# Maintenance Priority filter
# --------------------------------------------------

with filter_col4:

    priority_filter = st.selectbox(
        "Maintenance Priority",
        [
            "All",
            "Low",
            "Medium",
            "High",
            "Immediate"
        ]
    )


# --------------------------------------------------
# Filter reports
# --------------------------------------------------

filtered_reports = []

for report in reports:

    report_number = report.get(
        "report_number",
        ""
    )

    created_at = report.get(
        "created_at",
        ""
    )

    status = report.get(
        "status",
        "Unknown"
    )
    assessment = report.get(
        "assessment",
        {}
    )

    maintenance_priority = assessment.get(
        "maintenance_priority",
        ""
    )


    # ----------------------------------------------
    # Search filter
    # ----------------------------------------------

    if search_query:

        if search_query.lower() not in report_number.lower():
            continue

    # ----------------------------------------------
    # Status filter
    # ----------------------------------------------

    if status_filter != "All":

        if status != status_filter:
            continue

    # ----------------------------------------------
    # Maintenance Priority filter
    # ----------------------------------------------

    if priority_filter != "All":

        if maintenance_priority != priority_filter:
            continue

    # ----------------------------------------------
    # Date filter
    # ----------------------------------------------

    if date_filter:

        try:

            report_datetime = datetime.fromisoformat(
                created_at
            )

            if report_datetime.date() != date_filter:
                continue

        except Exception:

            continue

    filtered_reports.append(report)


# --------------------------------------------------
# Filter result count
# --------------------------------------------------

st.caption(
    f"Showing {len(filtered_reports)} of {len(reports)} reports"
)

st.divider()


# --------------------------------------------------
# No matching reports
# --------------------------------------------------

if not filtered_reports:

    st.warning(
        "No reports match the selected filters."
    )

    st.stop()


# --------------------------------------------------
# Display reports
# --------------------------------------------------

for report in filtered_reports:

    # ----------------------------------------------
    # Basic information
    # ----------------------------------------------

    report_number = report.get(
        "report_number",
        report["report_id"][:8]
    )

    created_at = report.get(
        "created_at",
        ""
    )

    status = report.get(
        "status",
        "Unknown"
    )

    detection_result = report.get(
        "detection_result",
        {}
    )

    total_damages = detection_result.get(
        "total_damages",
        0
    )

    # ----------------------------------------------
    # Format date/time
    # ----------------------------------------------

    try:

        report_datetime = datetime.fromisoformat(
            created_at
        )

        formatted_date = report_datetime.strftime(
            "%d %B %Y"
        )

        formatted_time = report_datetime.strftime(
            "%I:%M %p"
        )

    except Exception:

        formatted_date = created_at
        formatted_time = ""


    # ----------------------------------------------
    # Status indicator
    # ----------------------------------------------

    if status == "Completed":

        status_text = "🟢 Completed"

    elif status == "Pending":

        status_text = "🟡 Pending"

    else:

        status_text = f"⚪ {status}"


    # ----------------------------------------------
    # Report header
    # ----------------------------------------------

    with st.expander(
        f"📄 {report_number}  —  "
        f"{formatted_date}, {formatted_time}"
    ):

        # ------------------------------------------
        # Overview
        # ------------------------------------------

        st.subheader("Inspection Overview")

        overview_col1, overview_col2, overview_col3 = st.columns(
            3,
            gap="medium"
        )

        with overview_col1:

            st.metric(
                "Report ID",
                report_number
            )

        with overview_col2:

            st.metric(
                "Damages Detected",
                total_damages
            )

        with overview_col3:

            st.metric(
                "Status",
                status
            )
        # ------------------------------------------
        # Location
        # ------------------------------------------

        location = report.get(
            "location",
            {}
        )

        latitude = location.get(
            "latitude"
        )

        longitude = location.get(
            "longitude"
        )

        address = location.get(
            "address"
        )

        st.subheader("📍 Inspection Location")

        if latitude is not None and longitude is not None:

            st.write(
                f"**Coordinates:** "
                f"{latitude:.6f}, {longitude:.6f}"
            )

        else:

            st.info(
                "GPS location was not recorded for this inspection."
            )

        if address:

            st.write(
                f"**Address:** {address}"
            )

        st.divider()


        # ------------------------------------------
        # Annotated image
        # ------------------------------------------

        image_path = detection_result.get(
            "annotated_image"
        )

        if image_path:

            image_path = Path(image_path)

            if image_path.exists():

                st.subheader(
                    "🖼️ Inspection Image"
                )

                st.image(
                    str(image_path),
                    use_container_width=True
                )

            else:

                st.warning(
                    "Annotated inspection image is unavailable."
                )

        else:

            st.warning(
                "No annotated image is stored for this report."
            )


        st.divider()


        # ------------------------------------------
        # Damage summary
        # ------------------------------------------

        st.subheader(
            "🎯 Damage Summary"
        )

        detections = detection_result.get(
            "detections",
            []
        )

        if detections:

            damage_counts = Counter(
                d["damage_type"]
                .replace("_", " ")
                .title()
                for d in detections
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


        st.divider()


        # ------------------------------------------
        # AI report
        # ------------------------------------------

        st.subheader(
            "📝 Inspection Report"
        )

        ai_report = report.get(
            "ai_report"
        )

        if ai_report:

            st.markdown(
                ai_report
            )

        else:

            st.info(
                "No inspection report is available."
            )


        st.divider()


        # ------------------------------------------
        # PDF download
        # ------------------------------------------

        st.subheader(
            "📄 Download Report"
        )

        try:

            pdf_bytes = generate_pdf(
                report
            )

            st.download_button(
                label="Download PDF Report",
                data=pdf_bytes,
                file_name=f"{report_number}.pdf",
                mime="application/pdf",
                key=f"pdf_{report['report_id']}",
                use_container_width=True
            )

        except Exception as e:

            st.error(
                f"Unable to generate PDF report: {e}"
            )


        # ------------------------------------------
        # Status management
        # ------------------------------------------

        if status == "Pending":

            st.divider()

            if st.button(
                "✅ Mark as Completed",
                key=f"complete_{report['report_id']}",
                use_container_width=True
            ):

                db.update_status(
                    report["report_id"],
                    "Completed"
                )

                st.success(
                    "Report marked as completed."
                )

                st.rerun()

        elif status == "Completed":

            st.success(
                "✅ This inspection has been completed."
            )