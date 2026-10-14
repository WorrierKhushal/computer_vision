# Project Statement: SmartVision-Ed

**Project Title:** SmartVision-Ed &mdash; Computer Vision-Based Student Engagement, Attention Analytics & Academic Dropout Early Warning System  
**Author:** Khushal Mahajan  
**Registration Number:** 24MIM10014  
**Course Code / Name:** CSE3002 &mdash; Computer Vision  
**Academic Institution:** Vellore Institute of Technology (VIT)  

---

## 1. Problem Statement
In modern higher education institutions, large classroom sizes and hybrid/digital learning environments create a significant disconnect between instructor delivery and real-time student cognitive engagement. Instructors often cannot identify subtle, compounding patterns of student disengagement, chronic fatigue, and cognitive overload during lecture delivery. 

Traditional academic warning systems rely exclusively on lagging indicators&mdash;such as end-of-semester exam failures or post-facto attendance debarment notices (e.g., dropping below the mandatory 75% university attendance threshold). By the time these conventional alerts fire, student academic failure or course dropout is practically irreversible. 

There is an urgent necessity for an objective, non-intrusive, privacy-preserving, and proactive system capable of:
1. Monitoring real-time classroom visual attention dynamics using computer vision (without intrusive surveillance or human fatigue).
2. Quantifying physiological indicators of cognitive alertness, drowsiness, and distraction.
3. Fusing real-time visual attention telemetry with longitudinal academic performance records (attendance, internal assessment marks, and LMS engagement).
4. Generating early, actionable, and prescriptive dropout warnings to enable timely pedagogical and institutional interventions before failure occurs.

---

## 2. Scope of the Project
The scope of **SmartVision-Ed** encompasses the complete end-to-end pipeline from visual perception to multi-modal academic risk modeling:

- **Spatial-Temporal Vision Perception:**
  - Real-time video frame processing for facial localization and 68-point landmark geometry.
  - Ocular openness quantification using mathematical Eye Aspect Ratio (EAR) formulation for blink rate and micro-sleep detection.
  - 3D Head Pose estimation via Perspective-n-Point (`solvePnP`) decomposing rotation matrices into Euler angles (Yaw, Pitch, Roll) for gaze deviation tracking.
  - Mouth Aspect Ratio (MAR) formulation for involuntary yawn and fatigue detection.
  - Multi-cue cognitive and affective state classification (Focused, Distracted, Drowsy, Confused, Neutral).

- **Temporal Telemetry & Anonymization Engine:**
  - Exponential Moving Average (EMA) filtering to smooth high-frequency visual noise and saccadic eye movements.
  - State-machine event counters for sustained distraction episodes and drowsiness occurrences.
  - Salted SHA-256 cryptographic pseudonymization and automated Gaussian facial blurring to guarantee strict privacy preservation and compliance with academic data protection standards.

- **Multi-Modal Academic Vulnerability Modeling:**
  - Mathematical formulation of the Composite Academic Vulnerability Score (CAVS), weighted across Visual Attention (30%), Lecture Attendance (25%), Internal Assessments (25%), and LMS Activity (20%).
  - Automated categorization into risk tiers: *Low Risk*, *Moderate Risk*, and *Critical Early Warning*.
  - Rule-based and machine learning-backed root-cause diagnostic extraction and prescriptive pedagogical interventions.

- **Interactive Educator Dashboard & Reporting:**
  - High-performance FastAPI REST API layer.
  - Sleek, modern, dark-themed responsive web dashboard featuring live HUD overlays, temporal attention graphs, interactive student roster, and a "What-If" scenario risk simulator.
  - Automated 15-section academic project report PDF compilation.

---

## 3. Target Users
1. **Course Instructors & Professors:**
   - Gain objective, aggregated insights into classroom-wide lecture engagement.
   - Detect lecture segments where student confusion or fatigue peaks to adapt lecture pacing dynamically.
2. **Proctors & Academic Faculty Advisors:**
   - Receive proactive, early warning notifications for vulnerable students before university debarment (75% attendance) or midterm assessment failures occur.
   - View root-cause diagnostic breakdowns and targeted intervention recommendations.
3. **Department Heads & Academic Deans:**
   - Review cohort-level retention analytics, student success trajectories, and curriculum effectiveness metrics.
4. **Students:**
   - Receive constructive, privacy-preserving feedback regarding personal study habits and focus dynamics while their biometric identities remain cryptographically protected.

---

## 4. High-Level Features
1. **Ocular Fatigue & Drowsiness Tracker:** Precision EAR computation thresholded at 0.18 with temporal persistence tracking to detect micro-sleep episodes.
2. **3D Gaze & Head Orientation Estimator:** Real-time PnP geometric projection tracking student screen focus (Yaw $\le 22^\circ$, Pitch $\le 18^\circ$).
3. **Cognitive Affect Classifier:** Multi-cue Bayesian-rule classification categorizing attention into Focused, Distracted, Drowsy, Confused, and Neutral states.
4. **Temporal Noise Filtering:** EMA windowing ($\alpha = 0.25$) eliminating transient eye blinks from skewing overall session attention indices.
5. **Privacy-Preserving HUD:** Real-time facial ROI blurring and salted SHA-256 token generation ensuring zero raw student PII is exposed.
6. **Multi-Modal Risk Fusion Engine (CAVS):** Comprehensive score integrating computer vision attention telemetry with attendance, internal marks, and LMS activity.
7. **Early Debarment & Dropout Alerting:** Automatic flag generation for students below the 75% attendance threshold or with composite risk scores $\ge 58.0$.
8. **Interactive What-If Risk Simulator:** Interactive web UI sliders enabling academic advisors to simulate potential grade and attendance recovery trajectories.
9. **Automated Academic PDF Report Compilation:** Programmatic ReportLab script generating publication-grade documentation with full evaluation metrics.
