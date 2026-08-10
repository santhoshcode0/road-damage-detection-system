from io import BytesIO
from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    KeepTogether
)
from reportlab.lib import colors


def format_datetime(value):

    try:
        return datetime.fromisoformat(value).strftime(
            "%d %B %Y, %I:%M %p"
        )

    except Exception:
        return value


def clean_damage_name(name):

    return name.replace("_", " ").title()


def find_logo():

    """
    Locate the StreetScan logo.
    Expected location:

        ui/assets/logo_with_tagline.png
    """

    project_root = Path(__file__).resolve().parents[2]

    possible_paths = [
        project_root / "ui" / "assets" / "logo.png",
        project_root / "ui" / "assets" / "logo.jpg",
        project_root / "ui" / "assets" / "logo.jpeg",
        project_root / "assets" / "logo.png",
        project_root / "assets" / "logo.jpg",
        project_root / "assets" / "logo.jpeg",
    ]

    for path in possible_paths:

        if path.exists():
            return path

    return None


def generate_pdf(report):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm
    )

    # --------------------------------------------------
    # Styles
    # --------------------------------------------------

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontSize=20,
        leading=24,
        spaceAfter=8
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=6
    )

    subsection_style = ParagraphStyle(
        "Subsection",
        parent=styles["Heading3"],
        fontSize=11,
        leading=14,
        spaceBefore=6,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=5
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontSize=9,
        leading=12
    )

    # --------------------------------------------------
    # NEW: Disclaimer style
    # --------------------------------------------------

    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
        spaceBefore=4,
        spaceAfter=4,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#333333"),
        alignment=1
    )

    # --------------------------------------------------
    # Basic report information
    # --------------------------------------------------

    report_number = report.get(
        "report_number",
        report["report_id"][:8]
    )

    created_at = format_datetime(
        report.get("created_at", "")
    )

    status = report.get(
        "status",
        "Unknown"
    )

    detection_result = report["detection_result"]

    detections = detection_result.get(
        "detections",
        []
    )

    total_damages = detection_result.get(
        "total_damages",
        len(detections)
    )

    # --------------------------------------------------
    # Location
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Build PDF
    # --------------------------------------------------

    elements = []

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    elements.append(
        Paragraph(
            "StreetScan",
            title_style
        )
    )

    elements.append(
        Paragraph(
            "AI-Powered Road Inspection Report",
            body_style
        )
    )

    elements.append(
        Spacer(1, 0.2 * cm)
    )

    # --------------------------------------------------
    # Report information table
    # --------------------------------------------------

    info_data = [
        [
            Paragraph(
                "<b>Report Number</b>",
                small_style
            ),
            Paragraph(
                report_number,
                small_style
            )
        ],

        [
            Paragraph(
                "<b>Date & Time</b>",
                small_style
            ),
            Paragraph(
                created_at,
                small_style
            )
        ],

        [
            Paragraph(
                "<b>Status</b>",
                small_style
            ),
            Paragraph(
                status,
                small_style
            )
        ],

        [
            Paragraph(
                "<b>Total Damages</b>",
                small_style
            ),
            Paragraph(
                str(total_damages),
                small_style
            )
        ],

        [
            Paragraph(
                "<b>Location</b>",
                small_style
            ),
            Paragraph(
                address
                if address
                else "Not provided",
                small_style
            )
        ],

        [
            Paragraph(
                "<b>Coordinates</b>",
                small_style
            ),
            Paragraph(
                (
                    f"{latitude:.6f}, {longitude:.6f}"
                    if latitude is not None
                    and longitude is not None
                    else "Not recorded"
                ),
                small_style
            )
        ]
    ]

    info_table = Table(
        info_data,
        colWidths=[4.2 * cm, 11.5 * cm]
    )

    info_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#eeeeee")
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    elements.append(info_table)

    elements.append(
        Spacer(1, 0.5 * cm)
    )

    # --------------------------------------------------
    # Annotated Image
    # --------------------------------------------------

    elements.append(
        Paragraph(
            "Inspection Image",
            section_style
        )
    )

    image_path = detection_result.get(
        "annotated_image"
    )

    if image_path:

        try:

            image = Image(
                image_path,
                width=15.5 * cm,
                height=10.3 * cm,
                kind="proportional"
            )

            elements.append(image)

        except Exception:

            elements.append(
                Paragraph(
                    "Inspection image unavailable.",
                    body_style
                )
            )

    else:

        elements.append(
            Paragraph(
                "Inspection image unavailable.",
                body_style
            )
        )

    # --------------------------------------------------
    # Damage Summary
    # --------------------------------------------------

    elements.append(
        Paragraph(
            "Damage Summary",
            section_style
        )
    )

    if detections:

        damage_counts = {}

        for detection in detections:

            damage_type = clean_damage_name(
                detection["damage_type"]
            )

            damage_counts[damage_type] = (
                damage_counts.get(damage_type, 0) + 1
            )

        table_data = [
            [
                Paragraph("<b>Damage Type</b>", small_style),
                Paragraph("<b>Count</b>", small_style)
            ]
        ]

        for damage_type, count in damage_counts.items():

            table_data.append(
                [
                    Paragraph(
                        damage_type,
                        small_style
                    ),
                    Paragraph(
                        str(count),
                        small_style
                    )
                ]
            )

        damage_table = Table(
            table_data,
            colWidths=[11.5 * cm, 4 * cm]
        )

        damage_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#333333")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ])
        )

        elements.append(
            damage_table
        )

    else:

        elements.append(
            Paragraph(
                "No visible damage detected.",
                body_style
            )
        )

    # --------------------------------------------------
    # AI Inspection Report
    # --------------------------------------------------

    elements.append(
        Paragraph(
            "Inspection Assessment",
            section_style
        )
    )

    ai_report = report.get(
        "ai_report",
        ""
    )

    if ai_report:

        # Remove Markdown heading markers because
        # the PDF creates its own section formatting.
        lines = ai_report.splitlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # Section headings
            if line.startswith("## "):

                heading = line.replace(
                    "## ",
                    "",
                    1
                ).strip()

                elements.append(
                    Paragraph(
                        heading,
                        subsection_style
                    )
                )

            # Bullet points
            elif line.startswith("- "):

                bullet = line[2:].strip()

                elements.append(
                    Paragraph(
                        f"• {bullet}",
                        body_style
                    )
                )

            else:

                elements.append(
                    Paragraph(
                        line,
                        body_style
                    )
                )

    else:

        elements.append(
            Paragraph(
                "No inspection assessment available.",
                body_style
            )
        )

    # --------------------------------------------------
    # Detailed Detection Information
    # --------------------------------------------------

    if detections:

        elements.append(
            Paragraph(
                "Detection Details",
                section_style
            )
        )

        detection_table_data = [
            [
                Paragraph("<b>Damage Type</b>", small_style),
                Paragraph("<b>Confidence</b>", small_style)
            ]
        ]

        for detection in detections:

            damage_type = clean_damage_name(
                detection["damage_type"]
            )

            confidence = detection.get(
                "confidence",
                0
            ) * 100

            detection_table_data.append(
                [
                    Paragraph(
                        damage_type,
                        small_style
                    ),
                    Paragraph(
                        f"{confidence:.1f}%",
                        small_style
                    )
                ]
            )

        detection_table = Table(
            detection_table_data,
            colWidths=[11.5 * cm, 4 * cm]
        )

        detection_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#333333")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ])
        )

        elements.append(
            detection_table
        )

    # --------------------------------------------------
    # STREETSCAN LOGO + WARNING
    # --------------------------------------------------

    elements.append(
        Spacer(1, 0.7 * cm)
    )

    logo_path = find_logo()

    if logo_path:

        try:

            logo = Image(
                str(logo_path)
            )

            # Maximum dimensions for the logo
            max_width = 10 * cm
            max_height = 3.5 * cm

            # Preserve original aspect ratio
            aspect_ratio = (
                logo.imageWidth /
                logo.imageHeight
            )

            if aspect_ratio > (
                max_width / max_height
            ):

                logo.drawWidth = max_width
                logo.drawHeight = (
                    max_width / aspect_ratio
                )

            else:

                logo.drawHeight = max_height
                logo.drawWidth = (
                    max_height * aspect_ratio
                )

            # Center the logo
            logo.hAlign = "CENTER"

            elements.append(logo)

        except Exception:

            elements.append(
                Paragraph(
                    "StreetScan",
                    title_style
                )
            )

    else:

        # Fallback if the logo cannot be found
        elements.append(
            Paragraph(
                "StreetScan",
                ParagraphStyle(
                    "LogoFallback",
                    parent=title_style,
                    alignment=1
                )
            )
        )

    elements.append(
        Spacer(1, 0.25 * cm)
    )

    # --------------------------------------------------
    # Warning / Disclaimer
    # --------------------------------------------------

    elements.append(
        Paragraph(
            "<b>This report is based on visible surface defects "
            "identified in the inspected image and should not be "
            "treated as a structural engineering assessment.</b>",
            disclaimer_style
        )
    )

    # --------------------------------------------------
    # Generate PDF
    # --------------------------------------------------

    doc.build(elements)

    buffer.seek(0)

    return buffer.getvalue()