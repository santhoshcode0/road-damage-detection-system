# StreetScan

## AI-Powered Road Damage Inspection Platform

StreetScan is an AI-powered road inspection platform developed as part of the **Samsung Capstone Project**.

The platform analyzes uploaded road images using a custom-trained **YOLO11** computer vision model to identify visible road-surface damage. The detected damage is then processed through a structured assessment system to determine a preliminary road condition, maintenance risk, maintenance priority, and repair category.

Google Gemini is used to generate a professional, human-readable inspection report based on the detected damage and the structured assessment.

Inspection reports are stored in MongoDB and can be reviewed through the dashboard or exported as professional PDF documents.

> **Important:** StreetScan provides a preliminary visual surface inspection. It is not a structural engineering assessment and does not determine road or traffic safety.

---

## Features

### AI Road Damage Detection

StreetScan uses a custom-trained YOLO11 model to detect visible road-surface damage from uploaded images.

Supported damage categories:

- Longitudinal Crack
- Transverse Crack
- Alligator Crack
- Pothole
- Other Corruption

### Structured Damage Assessment

Detected damage is processed using a deterministic assessment system that calculates:

- Severity Score
- Road Condition
- Maintenance Risk
- Maintenance Priority
- Repair Category
- Damage Counts

The assessment system uses predefined damage weights rather than allowing the language model to independently determine the classification.

### AI Inspection Reports

Google Gemini generates a professional inspection report using the detected damage and the structured assessment.

Reports contain:

- Road Condition
- Summary
- Maintenance Risk
- Observed Damages
- Recommended Actions
- Maintenance Priority
- Conclusion

### Inspection History

Inspection reports are stored in MongoDB and can be accessed through the Reports section.

Users can:

- View previous inspections
- Search reports
- Filter reports
- Review detection results
- Review AI inspection reports
- Update report status
- Download PDF reports

### Duplicate Report Protection

StreetScan generates a SHA-256 hash for uploaded images.

If the same image has already been inspected, the system detects the duplicate and prevents another report from being created.

### Dashboard

The dashboard provides an overview of inspection activity, including:

- Total Reports
- Total Detected Damages
- Pending Reports
- Recent Inspections
- Damage Distribution

### PDF Reports

Inspection results can be exported as professional PDF reports containing the inspection information, detected damage, assessment, and recommendations.

---

# System Workflow

```text
                         Road Image
                              │
                              ▼
                    ┌─────────────────┐
                    │     YOLO11      │
                    │ Damage Detection│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Damage      │
                    │   Assessment    │
                    └────────┬────────┘
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
          Structured Results      Gemini Report
                  │                     │
                  └──────────┬──────────┘
                             ▼
                    ┌─────────────────┐
                    │     MongoDB     │
                    │     Storage     │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
                Dashboard         PDF Report
```

---

# Technology Stack

## Artificial Intelligence

- **YOLO11** — road damage detection
- **Google Gemini** — inspection report generation

## Programming Language

- **Python**

## Web Application

- **Streamlit**

## Database

- **MongoDB**

## Computer Vision

- **OpenCV**
- **Ultralytics**

## PDF Generation

- **ReportLab**

## Environment & Configuration

- **python-dotenv**

## Version Control

- **Git**
- **GitHub**

## Hardware Acceleration

- **CUDA**
- **NVIDIA GPU**

---

# Project Architecture

```text
StreetScan/
│
├── src/
│   ├── core/
│   │   ├── ai_report.py
│   │   ├── database.py
│   │   ├── damage_assessment.py
│   │   ├── detect.py
│   │   ├── pdf_generator.py
│   │   ├── pipeline.py
│   │   └── report_builder.py
│   │
│   ├── config.py
│   └── train.py
│
├── ui/
│   ├── pages/
│   │   ├── home.py
│   │   ├── upload.py
│   │   └── reports.py
│   │
│   ├── assets/
│   └── styles/
│
├── data/
│
├── storage/
│   └── outputs/
│
├── runs/
│   └── detect/
│       └── models/
│
├── streamlit_app.py
├── requirements.txt
├── README.md
└── .env
```

---

# Installation

## 1. Clone the Repository

```bash
git clone <https://github.com/santhoshcode0/road-damage-detection-system>
cd Samsung-Road-Damage-Detection-Assistant
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate the environment:

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key
MONGODB_URI=your_mongodb_connection_string
```

Do **not** commit `.env` to GitHub.

Make sure `.env` is included in `.gitignore`.

---

# Running StreetScan

Start the Streamlit application:

```bash
streamlit run streamlit_app.py
```

The application will open in your browser.

---

# Using StreetScan

## Step 1 — Upload a Road Image

Upload a clear image of the road surface.

Supported formats:

- JPG
- JPEG
- PNG

## Step 2 — Analyze the Road

StreetScan runs the uploaded image through the trained YOLO11 model.

The system identifies visible road damage and displays:

- Original image
- Annotated image
- Detected damage
- Damage count

## Step 3 — Review the Assessment

The system calculates a preliminary:

- Road Condition
- Maintenance Risk
- Maintenance Priority
- Repair Category

## Step 4 — Generate the Inspection Report

Google Gemini generates a professional inspection report based on the detected damage and structured assessment.

## Step 5 — Save the Inspection

The inspection is stored in MongoDB with a unique report number.

Example:

```text
REP-0001
```

## Step 6 — Review Previous Inspections

Previously generated reports can be accessed from the Reports section.

## Step 7 — Export the Report

The complete inspection can be downloaded as a PDF report.

---

# Machine Learning Model

StreetScan uses a custom-trained YOLO11 object detection model.

The model supports the following road-damage categories:

```text
Longitudinal Crack
Transverse Crack
Alligator Crack
Other Corruption
Pothole
```

Training was performed using GPU acceleration with CUDA.

Individual training runs and checkpoints are preserved so that different model versions can be compared without overwriting previous experiments.

The current production candidate is the best-performing checkpoint from the latest successful training run.

---

# Model Evaluation

The model is evaluated using standard object-detection metrics including:

- Precision
- Recall
- mAP@50
- mAP@50-95

These metrics are used to compare different training runs and determine the most suitable model checkpoint for StreetScan.

---

# Damage Assessment

StreetScan separates **machine-learning detection** from **application-level assessment**.

The YOLO11 model identifies visible road damage.

The damage assessment module then applies predefined damage weights to produce a preliminary severity score.

Current damage weights:

| Damage Type        | Weight |
| ------------------ | -----: |
| Pothole            |      4 |
| Alligator Crack    |      4 |
| Transverse Crack   |      2 |
| Longitudinal Crack |      2 |
| Other Corruption   |      1 |

The resulting score is used to determine:

```text
Severity Score
      │
      ▼
Road Condition
      │
      ▼
Maintenance Risk
      │
      ▼
Maintenance Priority
      │
      ▼
Repair Category
```

This separation keeps the assessment logic deterministic and independent of the AI report-generation system.

> The assessment weights are application heuristics and are not engineering severity standards.

---

# Database

StreetScan stores inspection reports in MongoDB.

A report can contain:

- Report ID
- Report Number
- Creation Timestamp
- Report Status
- Detection Results
- Damage Assessment
- AI Inspection Report
- Location Information
- Image Hash

The image hash is used to prevent duplicate inspections of the same uploaded image.

---

# Report Lifecycle

```text
Image Upload
     │
     ▼
Duplicate Check
     │
     ▼
YOLO11 Detection
     │
     ▼
Damage Assessment
     │
     ▼
Gemini Inspection Report
     │
     ▼
MongoDB Storage
     │
     ▼
Report Review
     │
     ▼
PDF Export
```

---

# Project Limitations

StreetScan is currently a **visual road-surface inspection system**.

It does not:

- Determine structural road integrity
- Determine whether a road is safe for traffic
- Perform physical pavement measurements
- Automatically estimate repair costs
- Predict future road deterioration
- Replace professional engineering inspection

Detection quality depends on factors such as:

- Image quality
- Lighting
- Camera angle
- Visibility of the road surface
- Damage size
- Damage appearance

---

# Future Development

Planned improvements include:

- Video-based road inspection
- Automatic frame extraction
- Damage tracking across video frames
- Geographic inspection mapping
- Road-damage heat maps
- Advanced inspection analytics
- Engineer review workflows
- Government API integration
- Email notifications
- Authentication
- Role-based access control
- Docker-based deployment
- Production deployment

---

# Project Status

## Artificial Intelligence

- [x] Dataset preparation
- [x] CUDA configuration
- [x] YOLO11 training
- [x] Damage detection pipeline
- [x] Structured damage assessment
- [x] Model evaluation

## Backend

- [x] Detection pipeline
- [x] MongoDB integration
- [x] Report generation
- [x] Duplicate image protection
- [x] PDF generation

## Frontend

- [x] Streamlit dashboard
- [x] Image upload
- [x] Detection visualization
- [x] Inspection summary
- [x] Report history
- [x] Search and filtering
- [x] Damage distribution

## AI Reporting

- [x] Gemini integration
- [x] Structured inspection reports
- [x] Maintenance recommendations

## Future

- [ ] Video inspection
- [ ] Authentication
- [ ] Role-based access
- [ ] Map integration
- [ ] Heat maps
- [ ] Production deployment

---

# Security

Sensitive credentials should be stored in environment variables rather than directly in source code.

The following should **never** be committed to GitHub:

```text
.env
API keys
MongoDB credentials
Private credentials
Large model checkpoints
Generated datasets
Temporary files
```

---

# Disclaimer

StreetScan is intended as a preliminary visual road-surface inspection and reporting tool.

The results are based on visible defects detected from uploaded imagery and should not be treated as a structural engineering assessment or a definitive determination of road or traffic safety.

---

# Samsung Capstone Project

Developed as part of the **Samsung Capstone Project**.

## StreetScan

**AI-Powered Road Damage Inspection Platform**
