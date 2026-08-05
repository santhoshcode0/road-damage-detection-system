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
        ai_report=None
    ):

        return {
            "report_id": str(uuid4()),
            "report_number": f"REP-{report_number:04d}",
            "created_at": datetime.now().isoformat(),
            "status": "Pending",
            "citizen_id": citizen_id,
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "address": address
            },
            "detection_result": detection_result,
            "ai_report": ai_report
        }