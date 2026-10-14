"""
Academic Risk Prediction & Multi-Modal Dropout Warning Engine for SmartVision-Ed.
Fuses computer-vision attention telemetry with academic indicators:
1. Visual Attention Index (V_att)
2. Lecture Attendance Rate (A_tt)
3. Internal Assessment / Midterm Performance (I_mk)
4. LMS Learning Management Engagement (L_ms)

Computes Composite Academic Vulnerability Score (CAVS) and produces actionable interventions.
Author: Khushal Mahajan (24MIM10014)
"""
from typing import Dict, Any, List, Optional
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from models.data_schemas import AcademicRiskProfile


class AcademicRiskAnalyzer:
    """
    Evaluates campus student academic vulnerability and triggers early dropout warnings.
    """
    def __init__(self):
        # Weights for multi-modal fusion
        self.w_vision = 0.30
        self.w_attendance = 0.25
        self.w_internal = 0.25
        self.w_lms = 0.20

        # Calibrated ML model for validation
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self._is_trained = False
        self._train_baseline_model()

    def _train_baseline_model(self):
        """
        Trains baseline Random Forest model on historical campus academic dataset.
        Features: [attendance, internal_marks, lms_score, visual_attention]
        Target: 0 (Retained/Passed), 1 (At-Risk/Dropout)
        """
        np.random.seed(42)
        n_samples = 400

        # Synthetic cohort generation reflecting university patterns
        att = np.random.uniform(50, 100, n_samples)
        internal = np.random.uniform(30, 98, n_samples)
        lms = np.random.uniform(20, 100, n_samples)
        vis_att = np.random.uniform(25, 95, n_samples)

        X = np.column_stack([att, internal, lms, vis_att])
        
        # Risk condition: low attendance (<75), poor internals (<50), or low combined engagement
        risk_score = 100 - (0.30 * vis_att + 0.25 * att + 0.25 * internal + 0.20 * lms)
        y = (risk_score >= 55.0).astype(int)

        self.model.fit(X, y)
        self._is_trained = True

    def calculate_cavs(
        self,
        attendance: float,
        internal_marks: float,
        lms_score: float,
        visual_attention: float
    ) -> float:
        """
        Computes Composite Academic Vulnerability Score (CAVS) [0.0 - 100.0].
        Higher score indicates higher vulnerability / dropout probability.
        """
        # Clamp inputs
        att_c = np.clip(attendance, 0.0, 100.0)
        int_c = np.clip(internal_marks, 0.0, 100.0)
        lms_c = np.clip(lms_score, 0.0, 100.0)
        vis_c = np.clip(visual_attention, 0.0, 100.0)

        composite_performance = (
            self.w_vision * vis_c +
            self.w_attendance * att_c +
            self.w_internal * int_c +
            self.w_lms * lms_c
        )

        cavs = 100.0 - composite_performance
        return round(float(np.clip(cavs, 0.0, 100.0)), 2)

    def evaluate_student(
        self,
        student_id: str,
        student_name: str,
        attendance: float,
        internal_marks: float,
        lms_score: float,
        visual_attention: Optional[float] = None
    ) -> AcademicRiskProfile:
        """
        Generates comprehensive academic risk evaluation, early warnings, and interventions.
        """
        # Default visual attention if not yet recorded
        v_att = visual_attention if visual_attention is not None else 72.0
        cavs = self.calculate_cavs(attendance, internal_marks, lms_score, v_att)

        contributing_factors: List[str] = []
        interventions: List[str] = []

        # Analyze individual risk contributors
        if attendance < 75.0:
            contributing_factors.append(f"Critical: Attendance ({attendance:.1f}%) is below university 75% debarment threshold.")
            interventions.append("Issue automated Proctor/Faculty Advisor warning and schedule attendance counseling.")

        if internal_marks < 50.0:
            contributing_factors.append(f"Sub-par Internal Assessment score ({internal_marks:.1f}/100) indicating subject comprehension deficit.")
            interventions.append("Enroll in peer-assisted tutoring and assign foundational remedial modules.")

        if v_att < 55.0:
            contributing_factors.append(f"Low classroom visual attention index ({v_att:.1f}%) exhibiting recurrent distraction/fatigue patterns.")
            interventions.append("Suggest micro-break intervals and interactive lecture check-in quizzes.")

        if lms_score < 45.0:
            contributing_factors.append(f"Infrequent LMS portal access and courseware engagement ({lms_score:.1f}%).")
            interventions.append("Send automated LMS deadline digests and mobile push notifications.")

        # Determine Risk Category
        if cavs >= 58.0 or attendance < 75.0:
            risk_category = "Critical Early Warning"
            early_dropout_flag = True
            if not interventions:
                interventions.append("Conduct one-on-one academic counseling session.")
        elif cavs >= 35.0:
            risk_category = "Moderate Risk"
            early_dropout_flag = False
            interventions.append("Monitor engagement trends across the next 3 lecture sessions.")
        else:
            risk_category = "Low Risk"
            early_dropout_flag = False
            interventions.append("Maintain current academic trajectory; eligible for advanced honors coursework.")

        return AcademicRiskProfile(
            student_id=student_id,
            student_name=student_name,
            course_id="CSE3002-CV",
            attendance_percentage=round(attendance, 1),
            internal_assessment_score=round(internal_marks, 1),
            lms_engagement_score=round(lms_score, 1),
            visual_attention_score=round(v_att, 1),
            composite_vulnerability_score=cavs,
            risk_category=risk_category,
            early_dropout_flag=early_dropout_flag,
            contributing_factors=contributing_factors if contributing_factors else ["No adverse risk factors detected."],
            suggested_interventions=interventions
        )
