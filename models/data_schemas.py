"""
Data models and schemas for SmartVision-Ed.
Author: Khushal Mahajan (24MIM10014)
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Point2D(BaseModel):
    x: float
    y: float


class HeadPoseAngles(BaseModel):
    yaw: float = Field(..., description="Head yaw angle in degrees (negative=left, positive=right)")
    pitch: float = Field(..., description="Head pitch angle in degrees (negative=down, positive=up)")
    roll: float = Field(..., description="Head roll angle in degrees (tilt)")
    is_facing_screen: bool = Field(..., description="True if student is looking towards display/camera")


class EyeAspectRatios(BaseModel):
    left_ear: float
    right_ear: float
    avg_ear: float
    is_blinking: bool
    is_drowsy: bool


class AffectClassification(BaseModel):
    dominant_state: str = Field(..., description="Primary affective state: Focused, Distracted, Drowsy, Neutral, Confused")
    confidence: float = Field(..., ge=0.0, le=1.0)
    state_distribution: Dict[str, float] = Field(default_factory=dict)


class FrameTelemetry(BaseModel):
    frame_index: int
    timestamp: float
    student_id: str
    anonymized_token: str
    head_pose: HeadPoseAngles
    eye_metrics: EyeAspectRatios
    affect: AffectClassification
    instantaneous_attention: float = Field(..., ge=0.0, le=100.0)
    smoothed_attention: float = Field(..., ge=0.0, le=100.0)


class SessionAttentionMetrics(BaseModel):
    student_id: str
    session_id: str
    duration_seconds: float
    frames_analyzed: int
    mean_attention_score: float
    focus_time_percentage: float
    distraction_event_count: int
    drowsiness_alert_count: int
    fatigue_index: float


class AcademicRiskProfile(BaseModel):
    student_id: str
    student_name: str
    course_id: str = "CSE3002-CV"
    attendance_percentage: float
    internal_assessment_score: float
    lms_engagement_score: float
    visual_attention_score: float
    composite_vulnerability_score: float = Field(..., ge=0.0, le=100.0)
    risk_category: str = Field(..., description="'Low Risk', 'Moderate Risk', 'Critical Early Warning'")
    early_dropout_flag: bool
    contributing_factors: List[str]
    suggested_interventions: List[str]


class IngestFrameRequest(BaseModel):
    student_id: str
    frame_base64: Optional[str] = None
    use_synthetic: bool = False
    synthetic_state: Optional[str] = None


class RiskEvaluationRequest(BaseModel):
    student_id: str
    attendance: float
    internal_marks: float
    lms_score: float
    visual_attention: Optional[float] = None
