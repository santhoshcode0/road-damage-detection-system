from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib import colors


def generate_pdf(report):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        fontSize=18,
        spaceAfter=6
    )
    label = styles["Heading3"]
    body = styles["BodyText"]

    elements = []

    report_number = report.get("report_number", report["report_id"][:8])

    elements.append(Paragraph("Road Damage Inspection Report", title_style))
    elements.append(Paragraph(f"Report Number: {report_number}", body))
    elements.append(Paragraph(f"Date: {report['created_at']}", body))
    elements.append(Paragraph(f"Status: {report['status']}", body))
    elements.append(Spacer(1, 0.5*cm))

    detection_result = report["detection_result"]

    elements.append(Paragraph("Annotated Image", label))
    try:
        elements.append(
            Image(detection_result["annotated_image"], width=15*cm, height=10*cm)
        )
    except Exception:
        elements.append(Paragraph("(Image unavailable)", body))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph("AI Inspection Report", label))
    elements.append(Paragraph(report["ai_report"].replace("\n", "<br/>"), body))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph("Detected Damages", label))

    detections = detection_result["detections"]
    if detections:
        table_data = [["Damage Type", "Confidence"]]
        for d in detections:
            table_data.append([
                d["damage_type"],
                f"{d['confidence']*100:.1f}%"
            ])

        table = Table(table_data, colWidths=[8*cm, 4*cm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#333333")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("No damage detected.", body))

    doc.build(elements)

    buffer.seek(0)
    return buffer.getvalue()