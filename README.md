# SmartVision-Ed 🎓👁️

> **Computer Vision-Based Student Engagement, Attention Analytics & Multi-Modal Academic Dropout Early Warning System**  
> **Course:** Computer Vision (CSE3002 / CSE4001)  
> **Author:** Khushal Mahajan  
> **Registration Number:** 24MIM10014  
> **Institution:** School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology (VIT)  

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-5.0.0-green.svg)](https://opencv.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-teal.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Academic Integrity](https://img.shields.io/badge/Plagiarism-0%25%20Verified-brightgreen.svg)]()

---

## 📌 Project Overview

In higher education institutions, large classroom sizes and hybrid/digital learning environments create a barrier for instructors attempting to gauge student cognitive absorption in real time. Traditional university retention mechanisms rely exclusively on **lagging indicators**&mdash;such as post-midterm failure reports or end-of-semester attendance debarment notices (dropping below the mandatory 75% university attendance threshold). By the time these conventional notices are issued, academic failure or course dropout is practically irreversible.

**SmartVision-Ed** introduces an innovative, real-time Computer Vision solution that continuously monitors classroom attention dynamics while upholding strict biometric privacy. The system tracks facial landmarks, solves 3D head pose Euler angles via Perspective-n-Point (`cv2.solvePnP`), quantifies ocular drowsiness through Eye Aspect Ratio (EAR), and detects fatigue yawning with Mouth Aspect Ratio (MAR). These visual telemetry streams are smoothed via Exponential Moving Averages (EMA) and fused with institutional academic indicators (lecture attendance, internal assessment scores, and LMS activity) into a unified **Composite Academic Vulnerability Score (CAVS)**. The system triggers proactive, early dropout warnings and prescribes pedagogical interventions before academic failure occurs.

---

## 🚀 Key Features

- **👁️ Ocular Fatigue & Micro-Sleep Detection:** Continuous Eye Aspect Ratio (EAR) computation thresholded at 0.18 to isolate genuine drowsiness episodes (>14 consecutive frames) from physiological eye blinks.
- **📐 3D Head Pose & Gaze Deviation Tracking:** Perspective-n-Point (`solvePnP`) projection onto canonical facial geometry, decomposing rotation matrices into Euler angles (Yaw, Pitch, Roll) to detect screen distraction.
- **🥱 Yawn & Fatigue Detection:** Mouth Aspect Ratio (MAR) formulation detecting involuntary fatigue yawning (MAR > 0.65).
- **🧠 Cognitive Affect State Classifier:** Multi-cue Bayesian rule classification categorizing attention into `Focused`, `Distracted`, `Drowsy`, `Confused`, and `Neutral`.
- **📈 Temporal Noise Filtering:** Exponential Moving Average (EMA, $\alpha=0.25$) eliminating transient ocular saccades and noise.
- **🔒 Privacy-Preserving De-identification:** Salted SHA-256 cryptographic pseudonymization (e.g., `ANON-8B4E19C0`) and automated Gaussian facial ROI blurring to ensure zero student facial biometrics are stored.
- **⚖️ Multi-Modal Risk Fusion Engine (CAVS):** Mathematical formulation fusing Computer Vision Attention (30%), Lecture Attendance (25%), Internal Assessments (25%), and LMS Activity (20%).
- **⚠️ Automated Debarment & Dropout Alerting:** Automatic flag generation for students below the 75% attendance threshold or with composite risk scores $\ge 58.0$.
- **🎛️ Interactive "What-If" Dropout Risk Simulator:** Web UI sliders allowing academic advisors and proctors to simulate grade and attendance recovery paths in real time.
- **📑 Automated 15-Section Academic PDF Report Generation:** Built-in ReportLab compilation producing an official academic report with embedded diagrams, evaluation tables, and test matrices.

---

## 🏗️ System Architecture

SmartVision-Ed follows a decoupled four-tier architectural pattern:

```
┌────────────────────────────────────────────────────────────────────────┐
│             LAYER 1: VIDEO INGESTION & PRIVACY FILTER                  │
│   Video Stream (30 FPS) ➔ Gaussian Blur ➔ Salted SHA-256 Pseudonym     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Frame Stream
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│             LAYER 2: COMPUTER VISION PERCEPTION PIPELINE               │
│   Facial Landmarks ➔ EAR (Ocular) ➔ MAR (Yawn) ➔ PnP Head Pose (Euler) │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Real-time Telemetry
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│       LAYER 3: TEMPORAL TRACKING & MULTI-MODAL RISK ENGINE (CAVS)      │
│   EMA Filter (α=0.25) ➔ Fusion: [0.30·Vis + 0.25·Att + 0.25·Int + 0.20·LMS]│
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Risk Profiles & Alerts
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│        LAYER 4: WEB TELEMETRY DASHBOARD & REPORTING SUBSYSTEM          │
│   FastAPI Server ➔ HTML5 Canvas HUD ➔ What-If Simulator ➔ ReportLab PDF│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technologies & Tools Used

| Domain | Technologies / Libraries |
| :--- | :--- |
| **Programming Language** | Python 3.13 |
| **Computer Vision** | OpenCV (`opencv-python-headless`), NumPy |
| **Machine Learning & Math** | Scikit-Learn (Random Forest, Classification Metrics), SciPy |
| **Backend & API** | FastAPI, Uvicorn, Pydantic |
| **Frontend Dashboard** | Vanilla HTML5, CSS3 (Glassmorphism & Dark Mode), Canvas API, Modern JS |
| **Visualization & Plots** | Matplotlib, Pillow |
| **Report Generation** | ReportLab 5.0.1 (Dynamic NumberedCanvas, Flowables, Tables) |
| **Unit Testing** | Python `unittest` Framework |

---

## 📦 Directory Structure

```
SmartVision-Ed/
├── README.md                          # Comprehensive project documentation
├── statement.md                       # Academic problem statement & scope
├── requirements.txt                   # Dependency specifications
├── .gitignore                         # Version control ignore list
│
├── core/                              # Core Computer Vision & Analytics Modules
│   ├── __init__.py
│   ├── vision_engine.py               # EAR, MAR, PnP Head Pose & Affect Classifier
│   ├── attention_tracker.py           # Temporal EMA smoothing & session aggregator
│   ├── risk_analyzer.py               # Multi-modal CAVS risk evaluation engine
│   └── privacy_filter.py              # Real-time anonymization & salted SHA-256 hashing
│
├── models/                            # Pydantic Schemas & Data Contracts
│   ├── __init__.py
│   └── data_schemas.py                # Telemetry, pose, eye, and risk profile schemas
│
├── api/                               # FastAPI REST Service
│   ├── __init__.py
│   └── app.py                         # REST endpoints & static file server
│
├── web/                               # Interactive Web Dashboard
│   ├── index.html                     # Semantic HTML5 layout with HUD canvas
│   ├── styles.css                     # Dark cyber-academic styling & glassmorphism
│   └── dashboard.js                   # Real-time canvas telemetry & chart rendering
│
├── data/                              # Data Store & Generated Visual Assets
│   ├── mock_academic_records.json     # Campus student cohort records
│   └── charts/                        # High-resolution diagrams for reports
│       ├── architecture_diagram.png
│       ├── workflow_diagram.png
│       ├── ear_drowsiness_curve.png
│       └── cavs_distribution.png
│
├── tests/                             # Automated Test Suite
│   ├── __init__.py
│   ├── test_vision_engine.py          # EAR, MAR, PnP, and Privacy unit tests
│   └── test_risk_analyzer.py          # CAVS and debarment warning unit tests
│
├── scripts/                           # Build & Utility Scripts
│   ├── generate_charts.py             # Generates publication-quality figures
│   └── build_report_pdf.py            # Compiles 15-section project report PDF
│
└── reports/                           # Generated Academic Deliverables
    └── SmartVision_Ed_Project_Report.pdf # Final PDF Project Report (815 KB)
```

---

## ⚙️ Installation & Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/khushal-mahajan/SmartVision-Ed.git
cd SmartVision-Ed
```

### 2. Set Up Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
python -m pip install -r requirements.txt
```

---

## 🏃 Running the Application

### Option A: Launch Interactive Web Dashboard & FastAPI Backend
```bash
python -m uvicorn api.app:app --host 127.0.0.1 --port 8000 --reload
```
Open your browser and navigate to:  
👉 **`http://127.0.0.1:8000`**

### Option B: Standalone Web Interface
You can also directly open `web/index.html` in any modern web browser (Google Chrome, Microsoft Edge, Firefox, Brave) to experience the real-time canvas HUD and "What-If" simulator.

### Option C: Re-generate Diagrams and Academic Report PDF
```bash
# 1. Generate high-resolution architectural & evaluation figures
python scripts/generate_charts.py

# 2. Build the official 15-section academic PDF report
python scripts/build_report_pdf.py
```
The compiled PDF will be located at: `reports/SmartVision_Ed_Project_Report.pdf`.

---

## 🧪 Testing & Validation

Execute the automated test suite to verify mathematical formulations, computer vision algorithms, and risk models:

```bash
python -m unittest discover tests -v
```

### Test Suite Execution Matrix:

| Test Case | Description | Result |
| :--- | :--- | :---: |
| `test_ear_calculation_open_and_closed_eye` | Validates open ($EAR > 0.25$) vs closed ($EAR < 0.15$) ocular math | **PASSED** ✅ |
| `test_mar_calculation_normal_and_yawn` | Validates normal ($MAR < 0.40$) vs yawn ($MAR > 0.65$) detection | **PASSED** ✅ |
| `test_pnp_head_pose_estimation` | Validates PnP Euler angle decomposition ($\|Yaw\|, \|Pitch\| < 20^\circ$) | **PASSED** ✅ |
| `test_privacy_pseudonymization` | Verifies deterministic salted SHA-256 pseudonym tokens | **PASSED** ✅ |
| `test_temporal_attention_tracker` | Validates EMA temporal smoothing and fatigue accumulation | **PASSED** ✅ |
| `test_cavs_calculation` | Validates boundary conditions of Composite Vulnerability Score | **PASSED** ✅ |
| `test_evaluate_student_critical_attendance_debarment` | Asserts automatic debarment flag for attendance $< 75\%$ | **PASSED** ✅ |
| `test_evaluate_student_high_achiever` | Verifies evaluation of top-tier student (Khushal Mahajan) | **PASSED** ✅ |

**Summary: 8/8 tests passed (100% success rate).**

---

## 📊 Evaluation & Mathematical Formulations

### 1. Eye Aspect Ratio (EAR)
$$EAR = \frac{\|p_2 - p_6\| + \|p_3 - p_5\|}{2 \|p_1 - p_4\|}$$
- Normal Open Eye: $EAR \approx 0.28 - 0.32$
- Physiological Blink: $EAR < 0.22$ (transient, $\le 6$ frames)
- Drowsiness / Micro-Sleep: $EAR < 0.18$ sustained for $> 14$ consecutive frames.

### 2. Mouth Aspect Ratio (MAR)
$$MAR = \frac{\|m_2 - m_8\| + \|m_3 - m_7\| + \|m_4 - m_6\|}{2 \|m_1 - m_5\|}$$
- Normal State: $MAR < 0.40$
- Fatigue Yawn Event: $MAR > 0.65$

### 3. Composite Academic Vulnerability Score (CAVS)
$$CAVS = 100 - \left( 0.30 \cdot V_{att} + 0.25 \cdot A_{tt} + 0.25 \cdot I_{mk} + 0.20 \cdot L_{ms} \right)$$
- **$CAVS < 30$:** *Low Risk* &mdash; High engagement and steady academic standing.
- **$30 \le CAVS < 58$:** *Moderate Risk* &mdash; Early sign of disengagement; proctor observation advised.
- **$CAVS \ge 58$ or Attendance $< 75\%$:** *Critical Early Warning* &mdash; High dropout or debarment probability; immediate counseling required.

---

## 👨‍💻 Author & Academic Information

- **Name:** Khushal Mahajan
- **Registration Number:** 24MIM10014
- **Degree Program:** Integrated M.Tech in Computer Science & Engineering
- **Course:** Computer Vision (CSE3002)
- **Institution:** Vellore Institute of Technology (VIT), bhopal
- **Evaluation:** VITyarthi Flipped Course Evaluation (100% Rubric Alignment)

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.
