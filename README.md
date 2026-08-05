# Road Damage Detection System

An AI-powered web application for detecting road damages from images using YOLO object detection. Users can upload road images, detect damages such as cracks and potholes, and store reports for future reference.

> Developed as a Samsung Capstone Project.

---

## Features

- Detect road damages from uploaded images
- Support for multiple damage types
- Display annotated detection results
- Store reports in MongoDB
- View previously reported damages
- Interactive web interface built with Streamlit

---

## Tech Stack

### Artificial Intelligence

- YOLO11 (Ultralytics)

### Backend

- Python

### Computer Vision

- OpenCV

### Database

- MongoDB

### Frontend

- Streamlit

### Development Tools

- Git
- GitHub
- Visual Studio Code

---

## Project Structure

```
Road-Damage-Detection-System
│
├── data/
├── models/
├── src/
│   ├── core/
│   ├── config.py
│   └── utils.py
│
├── storage/
│
├── ui/
│   └── pages/
│
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

## Current Workflow

```
Home
   ↓
Upload Image
   ↓
Road Damage Detection
   ↓
Detection Results
   ↓
Save Report
   ↓
View All Reports
```

---

## Road Damage Classes

- Longitudinal Crack
- Transverse Crack
- Alligator Crack
- Pothole

---

## Future Enhancements

- AI-generated inspection reports
- Interactive maps
- Authentication
- Road inspector dashboard
- Report analytics
- Email notifications
- PDF report generation

---

## Status

The project is currently under active development as part of the Samsung Capstone Project.
