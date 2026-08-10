import base64
import sys
from pathlib import Path
from collections import Counter

import streamlit as st


# ==================================================
# Project paths
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


# ==================================================
# Imports
# ==================================================

from core.database import Database


# ==================================================
# Page styling
# ==================================================

st.markdown(
    """
    <style>

    .dashboard-title {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .dashboard-subtitle {
        color: #9CA3AF;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .severity-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
    }

    .good {
        background: #166534;
        color: #DCFCE7;
    }

    .moderate {
        background: #92400E;
        color: #FEF3C7;
    }

    .critical {
        background: #991B1B;
        color: #FEE2E2;
    }

    .unknown {
        background: #4B5563;
        color: #F3F4F6;
    }

    .report-meta {
        color: #9CA3AF;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# Logo
# ==================================================

logo_path = Path("ui/assets/logo_with_tagline.png")
logo_base64 = base64.b64encode(logo_path.read_bytes()).decode()

st.markdown(
    f"""
<div style="
    width:100%;
    min-height:220px;
    background:#2c2f3a;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.08);
    display:flex;
    justify-content:center;
    align-items:center;
    padding:25px;
    margin-bottom:30px;
">
    <img
        src="data:image/png;base64,{logo_base64}"
        style="
            width:520px;
            max-width:90%;
            height:auto;
        "
    />
</div>
""",
    unsafe_allow_html=True,
)
st.write("")


# ==================================================
# Page Header
# ==================================================

st.markdown(
    '<div class="dashboard-title">StreetScan Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Road inspection overview and recent activity.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ==================================================
# Load database
# ==================================================

total_reports = 0
total_damages = 0
pending_reports = 0
critical_reports = 0

recent_reports = []
all_reports = []

try:

    db = Database()

    stats = db.get_stats()

    total_reports = stats["total_reports"]

    total_damages = stats["total_damages"]

    pending_reports = stats["pending_reports"]

    recent_reports = db.get_recent_reports(5)

    all_reports = db.get_all_reports()

    # ----------------------------------------------
    # Count critical inspections
    # ----------------------------------------------

    for report in all_reports:

        assessment = report.get(
            "assessment",
            {}
        )

        road_condition = assessment.get(
            "road_condition"
        )

        if road_condition == "Critical":

            critical_reports += 1


except Exception as e:

    st.error(
        "Unable to load dashboard data."
    )

    st.exception(e)


# ==================================================
# Dashboard Metrics
# ==================================================

st.markdown(
    '<div class="section-title">Inspection Overview</div>',
    unsafe_allow_html=True
)

metric1, metric2, metric3, metric4 = st.columns(
    4,
    gap="medium"
)


with metric1:

    st.metric(
        "Total Inspections",
        total_reports
    )


with metric2:

    st.metric(
        "Damages Detected",
        total_damages
    )


with metric3:

    st.metric(
        "Critical Inspections",
        critical_reports
    )


with metric4:

    st.metric(
        "Pending Reviews",
        pending_reports
    )


# ==================================================
# Recent Inspections
# ==================================================

st.markdown(
    '<div class="section-title">Recent Inspections</div>',
    unsafe_allow_html=True
)

if recent_reports:

    for report in recent_reports:

        report_number = report.get(
            "report_number",
            report.get(
                "report_id",
                "Unknown"
            )[:8]
        )

        created_at = report.get(
            "created_at"
        )

        # ------------------------------------------
        # Format date
        # ------------------------------------------

        formatted_date = "Unknown date"

        if created_at:

            try:

                from datetime import datetime

                dt = datetime.fromisoformat(
                    created_at
                )

                formatted_date = dt.strftime(
                    "%d/%m/%Y, %I:%M %p"
                )

            except Exception:

                formatted_date = created_at


        # ------------------------------------------
        # Damage information
        # ------------------------------------------

        detection_result = report.get(
            "detection_result",
            {}
        )

        detections = detection_result.get(
            "detections",
            []
        )

        damage_count = len(
            detections
        )


        # ------------------------------------------
        # Assessment
        # ------------------------------------------

        assessment = report.get(
            "assessment",
            {}
        )

        road_condition = assessment.get(
            "road_condition",
            "Unknown"
        )

        risk_level = assessment.get(
            "risk_level",
            "Unknown"
        )

        maintenance_priority = assessment.get(
            "maintenance_priority",
            "Unknown"
        )


        # ------------------------------------------
        # Severity badge
        # ------------------------------------------

        if road_condition == "Good":

            badge_class = "good"

        elif road_condition == "Moderate":

            badge_class = "moderate"

        elif road_condition == "Critical":

            badge_class = "critical"

        else:

            badge_class = "unknown"


        # ------------------------------------------
        # Location
        # ------------------------------------------

        location = report.get(
            "location",
            {}
        )

        address = location.get(
            "address"
        )


        # ------------------------------------------
        # Report card
        # ------------------------------------------

        with st.container(
            border=True
        ):

            card_col1, card_col2, card_col3 = st.columns(
                [3, 4, 2],
                gap="medium"
            )


            # --------------------------------------
            # Report number
            # --------------------------------------

            with card_col1:

                st.markdown(
                    f"### 📄 {report_number}"
                )

                st.markdown(
                    f'<div class="report-meta">'
                    f'{formatted_date}'
                    f'</div>',
                    unsafe_allow_html=True
                )


            # --------------------------------------
            # Inspection information
            # --------------------------------------

            with card_col2:

                if damage_count == 0:

                    damage_text = (
                        "No visible damage"
                    )

                elif damage_count == 1:

                    damage_text = (
                        "1 damage detected"
                    )

                else:

                    damage_text = (
                        f"{damage_count} damages detected"
                    )

                st.write(
                    damage_text
                )

                if address:

                    st.markdown(
                        f"📍 {address}"
                    )

                else:

                    st.markdown(
                        '<div class="report-meta">'
                        '📍 Location not recorded'
                        '</div>',
                        unsafe_allow_html=True
                    )


            # --------------------------------------
            # Severity
            # --------------------------------------

            with card_col3:

                st.markdown(
                    f"""
                    <span class="
                        severity-badge
                        {badge_class}
                    ">
                        {road_condition}
                    </span>
                    """,
                    unsafe_allow_html=True
                )

                st.write("")

                st.caption(
                    f"Risk: {risk_level}"
                )

                st.caption(
                    f"Priority: {maintenance_priority}"
                )


else:

    st.info(
        "No inspections available yet."
    )


# ==================================================
# Damage Distribution
# ==================================================

st.markdown(
    '<div class="section-title">Damage Distribution</div>',
    unsafe_allow_html=True
)


damage_counter = Counter()


for report in all_reports:

    detection_result = report.get(
        "detection_result",
        {}
    )

    detections = detection_result.get(
        "detections",
        []
    )

    for detection in detections:

        damage_type = (
            detection.get(
                "damage_type",
                "Unknown"
            )
            .replace("_", " ")
            .title()
        )

        damage_counter[
            damage_type
        ] += 1


if damage_counter:

    damage_data = {
        "Damage Type": list(
            damage_counter.keys()
        ),
        "Count": list(
            damage_counter.values()
        )
    }

    import altair as alt
    import pandas as pd

    if damage_counter:

        damage_data = pd.DataFrame({
            "Damage Type": list(
                damage_counter.keys()
            ),
            "Count": list(
                damage_counter.values()
            )
        })

        chart = alt.Chart(
            damage_data
        ).mark_bar().encode(
            x=alt.X(
                "Damage Type:N",
                title="Damage Type",
                axis=alt.Axis(
                    labelAngle=0
                )
            ),
            y=alt.Y(
                "Count:Q",
                title="Count"
            )
        )

        st.altair_chart(
            chart,
            use_container_width=True
        )

    else:

        st.info(
            "No damage data available yet."
        )

else:

    st.info(
        "No damage data available yet."
    )


# ==================================================
# Navigation
# ==================================================

st.divider()

st.markdown(
    '<div class="section-title">Quick Actions</div>',
    unsafe_allow_html=True
)

action_col1, action_col2 = st.columns(
    2,
    gap="medium"
)


with action_col1:

    if st.button(
        "🔍 Start New Inspection",
        use_container_width=True,
        type="primary"
    ):

        st.switch_page(
            "ui/pages/upload.py"
        )


with action_col2:

    if st.button(
        "📄 View All Reports",
        use_container_width=True
    ):

        st.switch_page(
            "ui/pages/reports.py"
        )