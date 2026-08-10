from datetime import datetime
from uuid import uuid4


class ReportBuilder:

    @staticmethod
    def build(
        detection_result,
        report_number,
        citizen_id=None,
        latitude=None,
        longitude=None,
        address=None,
        ai_report=None,
        assessment=None,
        image_hash=None
    ):

        return {

            # ------------------------------------------
            # Unique report identifier
            # ------------------------------------------

            "report_id": str(
                uuid4()
            ),

            # ------------------------------------------
            # Human-readable report number
            # ------------------------------------------

            "report_number": (
                f"REP-{report_number:04d}"
            ),

            # ------------------------------------------
            # Creation timestamp
            # ------------------------------------------

            "created_at": (
                datetime.now().isoformat()
            ),

            # ------------------------------------------
            # Report status
            # ------------------------------------------

            "status": "Pending",

            # ------------------------------------------
            # Citizen information
            # ------------------------------------------

            "citizen_id": citizen_id,

            # ------------------------------------------
            # Location
            # ------------------------------------------

            "location": {

                "latitude": latitude,

                "longitude": longitude,

                "address": address
            },

            # ------------------------------------------
            # Image hash
            # ------------------------------------------

            "image_hash": image_hash,

            # ------------------------------------------
            # Detection result
            # ------------------------------------------

            "detection_result": (
                detection_result
            ),

            # ------------------------------------------
            # Structured assessment
            # ------------------------------------------

            "assessment": assessment,

            # ------------------------------------------
            # AI-generated report
            # ------------------------------------------

            "ai_report": ai_report
        }