"""
FastAPI Server for SmartVision-Ed.
Provides RESTful APIs for real-time video telemetry ingestion, student risk evaluation,
and web dashboard monitoring.
Author: Khushal Mahajan (24MIM10014)
"""
import os
import json
import base64
from typing import List, Dict, Any, Optional
import numpy as np
import cv2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from models.data_schemas import (
    IngestFrameRequest,
    RiskEvaluationRequest,
    AcademicRiskProfile,
    FrameTelemetry,
    SessionAttentionMetrics,
)
from core.vision_engine import ComputerVisionEngine
from core.attention_tracker import AttentionTracker
from core.risk_analyzer import AcademicRiskAnalyzer

app = FastAPI(
    title="SmartVision-Ed API",
    description="Computer Vision-Based Student Engagement & Academic Dropout Warning System",
    version="1.0.0",
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Core Services
vision_engine = ComputerVisionEngine(anonymize=False)
risk_analyzer = AcademicRiskAnalyzer()
active_trackers: Dict[str, AttentionTracker] = {}

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "mock_academic_records.json")


def load_students_data() -> List[Dict[str, Any]]:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "system": "SmartVision-Ed",
        "author": "Khushal Mahajan",
        "registration_number": "24MIM10014",
        "course": "Computer Vision (CSE3002)",
    }


@app.get("/api/students", response_model=List[AcademicRiskProfile])
def get_all_student_profiles():
    raw_data = load_students_data()
    results = []
    for s in raw_data:
        prof = risk_analyzer.evaluate_student(
            student_id=s["student_id"],
            student_name=s["student_name"],
            attendance=s["attendance_percentage"],
            internal_marks=s["internal_assessment_score"],
            lms_score=s["lms_engagement_score"],
            visual_attention=s.get("visual_attention_score")
        )
        results.append(prof)
    return results


@app.get("/api/students/{student_id}", response_model=AcademicRiskProfile)
def get_student_profile(student_id: str):
    raw_data = load_students_data()
    for s in raw_data:
        if s["student_id"].upper() == student_id.upper():
            return risk_analyzer.evaluate_student(
                student_id=s["student_id"],
                student_name=s["student_name"],
                attendance=s["attendance_percentage"],
                internal_marks=s["internal_assessment_score"],
                lms_score=s["lms_engagement_score"],
                visual_attention=s.get("visual_attention_score")
            )
    raise HTTPException(status_code=404, detail=f"Student {student_id} not found in database")


@app.post("/api/evaluate-risk", response_model=AcademicRiskProfile)
def evaluate_custom_risk(req: RiskEvaluationRequest):
    return risk_analyzer.evaluate_student(
        student_id=req.student_id,
        student_name="Evaluated Student",
        attendance=req.attendance,
        internal_marks=req.internal_marks,
        lms_score=req.lms_score,
        visual_attention=req.visual_attention
    )


@app.post("/api/analyze-frame")
def analyze_frame(req: IngestFrameRequest):
    """
    Ingests and processes a video frame, or generates a realistic synthetic frame with HUD telemetry.
    """
    student_id = req.student_id
    if student_id not in active_trackers:
        active_trackers[student_id] = AttentionTracker(student_id=student_id)

    tracker = active_trackers[student_id]
    frame_idx = tracker.total_frames + 1

    # Decode or create canvas
    if req.frame_base64:
        try:
            img_bytes = base64.b64decode(req.frame_base64.split(",")[-1])
            nparr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except Exception:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
    else:
        # Create dark studio background for simulation
        frame = np.full((480, 640, 3), 28, dtype=np.uint8)
        # Subtle gradient grid
        for gy in range(0, 480, 40):
            cv2.line(frame, (0, gy), (640, gy), (36, 40, 48), 1)
        for gx in range(0, 640, 40):
            cv2.line(frame, (gx, 0), (gx, 480), (36, 40, 48), 1)

    # Process frame through Vision Engine
    telemetry, annotated = vision_engine.process_frame(
        frame=frame,
        frame_index=frame_idx,
        student_id=student_id,
        simulated_state=req.synthetic_state
    )

    # Update Temporal Tracker
    smoothed_telemetry = tracker.update(telemetry)

    # Encode annotated frame to JPEG base64
    _, buffer = cv2.imencode(".jpg", annotated, [cv2.IMWRITE_JPEG_QUALITY, 85])
    annotated_b64 = base64.b64encode(buffer).decode("utf-8")

    return {
        "telemetry": smoothed_telemetry.dict(),
        "annotated_frame_base64": f"data:image/jpeg;base64,{annotated_b64}",
        "session_summary": tracker.get_session_summary().dict(),
    }


@app.get("/api/classroom-summary")
def get_classroom_summary():
    profiles = get_all_student_profiles()
    total = len(profiles)
    if total == 0:
        return {"total_students": 0}

    critical_count = sum(1 for p in profiles if p.risk_category == "Critical Early Warning")
    moderate_count = sum(1 for p in profiles if p.risk_category == "Moderate Risk")
    low_count = sum(1 for p in profiles if p.risk_category == "Low Risk")

    avg_attendance = np.mean([p.attendance_percentage for p in profiles])
    avg_attention = np.mean([p.visual_attention_score for p in profiles])
    avg_cavs = np.mean([p.composite_vulnerability_score for p in profiles])

    return {
        "total_enrolled": total,
        "critical_early_warnings": critical_count,
        "moderate_risk_students": moderate_count,
        "low_risk_students": low_count,
        "average_attendance": round(float(avg_attendance), 2),
        "average_classroom_attention": round(float(avg_attention), 2),
        "mean_vulnerability_score": round(float(avg_cavs), 2),
    }


# Mount Web Directory
web_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web")
if os.path.exists(web_dir):
    app.mount("/static", StaticFiles(directory=web_dir), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(web_dir, "index.html"))
