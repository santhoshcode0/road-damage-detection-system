import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from core.database import Database
from core.pdf_generator import generate_pdf

st.title("All Reports")

db = Database()
reports = db.get_all_reports()

if not reports:
    st.info("No reports found yet. Upload an image to generate one.")
else:
    for report in reports:
        label = report.get("report_number", report["report_id"][:8])

        with st.expander(f"{label} — {report['created_at']}"):
            st.write(f"**Status:** {report['status']}")
            st.write(
                f"**Total Damages:** "
                f"{report['detection_result']['total_damages']}"
            )

            st.image(
                report["detection_result"]["annotated_image"],
                use_container_width=True
            )

            st.write("**AI Inspection Report:**")
            st.write(report["ai_report"])

            st.write("**Detections:**")
            st.dataframe(
                report["detection_result"]["detections"],
                use_container_width=True,
                hide_index=True
            )

            pdf_bytes = generate_pdf(report)
            st.download_button(
                label="Download PDF Report",
                data=pdf_bytes,
                file_name=f"{label}.pdf",
                mime="application/pdf",
                key=f"pdf_{report['report_id']}",
                use_container_width=True
            )