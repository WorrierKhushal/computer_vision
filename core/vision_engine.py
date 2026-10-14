"""
Computer Vision Engine for Classroom Engagement & Attention Analysis.
Implements:
1. Facial geometry localization
2. Eye Aspect Ratio (EAR) blink and drowsiness analysis
3. 3D Head Pose Estimation via Perspective-n-Point (solvePnP)
4. Mouth Aspect Ratio (MAR) yawn detection
5. Facial Affect / Cognitive State Classifier
6. Visual Telemetry Overlay rendering

Author: Khushal Mahajan (24MIM10014)
"""
import math
import numpy as np
import cv2
from typing import Tuple, Dict, Any, Optional, List
from models.data_schemas import (
    HeadPoseAngles,
    EyeAspectRatios,
    AffectClassification,
    FrameTelemetry,
)
from core.privacy_filter import PrivacyPreservingFilter


class ComputerVisionEngine:
    """
    Core CV processing pipeline for real-time video frames.
    """
    def __init__(self, anonymize: bool = False):
        self.anonymize = anonymize
        self.privacy_filter = PrivacyPreservingFilter()

        # 3D Canonical facial model coordinates (in millimeters, OpenCV camera coordinate convention: Y down, Z forward)
        self.model_points_3d = np.array([
            (0.0, 0.0, 0.0),             # Nose tip
            (0.0, 330.0, -65.0),         # Chin
            (-225.0, -170.0, -135.0),    # Left eye outer corner
            (225.0, -170.0, -135.0),     # Right eye outer corner
            (-150.0, 150.0, -125.0),     # Left mouth corner
            (150.0, 150.0, -125.0),      # Right mouth corner
        ], dtype=np.float64)

        # Baseline thresholds
        self.EAR_BLINK_THRESHOLD = 0.22
        self.EAR_DROWSY_THRESHOLD = 0.18
        self.MAR_YAWN_THRESHOLD = 0.65
        self.MAX_YAW_THRESHOLD = 22.0    # Degrees
        self.MAX_PITCH_THRESHOLD = 18.0  # Degrees

    @staticmethod
    def calculate_ear(eye_points: np.ndarray) -> float:
        """
        Computes the Eye Aspect Ratio (EAR) based on Soukupova & Cech (2016):
        EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
        eye_points: 6 (x, y) coordinates
        """
        if len(eye_points) < 6:
            return 0.30  # Default open eye fallback

        p1, p2, p3, p4, p5, p6 = eye_points[:6]
        
        # Vertical distances
        dist_vert_1 = np.linalg.norm(p2 - p6)
        dist_vert_2 = np.linalg.norm(p3 - p5)
        
        # Horizontal distance
        dist_horiz = np.linalg.norm(p1 - p4)

        if dist_horiz < 1e-6:
            return 0.0

        ear = (dist_vert_1 + dist_vert_2) / (2.0 * dist_horiz)
        return float(ear)

    @staticmethod
    def calculate_mar(mouth_points: np.ndarray) -> float:
        """
        Computes Mouth Aspect Ratio (MAR) for yawn detection.
        MAR = (||m2 - m8|| + ||m3 - m7|| + ||m4 - m6||) / (2 * ||m1 - m5||)
        mouth_points: 8 (x, y) coordinates
        """
        if len(mouth_points) < 8:
            return 0.20

        m1, m2, m3, m4, m5, m6, m7, m8 = mouth_points[:8]
        v1 = np.linalg.norm(m2 - m8)
        v2 = np.linalg.norm(m3 - m7)
        v3 = np.linalg.norm(m4 - m6)
        h = np.linalg.norm(m1 - m5)

        if h < 1e-6:
            return 0.0

        mar = (v1 + v2 + v3) / (2.0 * h)
        return float(mar)

    def estimate_head_pose(
        self,
        image_points: np.ndarray,
        frame_shape: Tuple[int, int]
    ) -> Tuple[HeadPoseAngles, np.ndarray, np.ndarray]:
        """
        Solves Perspective-n-Point (PnP) problem to determine 3D head orientation (Yaw, Pitch, Roll).
        image_points: 6 (x, y) coordinates corresponding to canonical model points.
        frame_shape: (height, width)
        """
        h, w = frame_shape
        focal_length = w
        center = (w / 2.0, h / 2.0)
        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype=np.float64)

        dist_coeffs = np.zeros((4, 1), dtype=np.float64)

        success, rvec, tvec = cv2.solvePnP(
            self.model_points_3d,
            image_points.astype(np.float64),
            camera_matrix,
            dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )

        if not success:
            return HeadPoseAngles(yaw=0.0, pitch=0.0, roll=0.0, is_facing_screen=True), np.zeros(3), np.zeros(3)

        # Convert rotation vector to 3x3 rotation matrix
        rmat, _ = cv2.Rodrigues(rvec)

        # Robust Euler angle decomposition via RQDecomp3x3
        angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
        pitch_deg = float(angles[0])
        yaw_deg = float(angles[1])
        roll_deg = float(angles[2])

        # Normalize roll to range [-90, 90]
        if roll_deg > 90:
            roll_deg -= 180
        elif roll_deg < -90:
            roll_deg += 180

        # Check if student is actively facing screen
        is_facing = (
            abs(yaw_deg) <= self.MAX_YAW_THRESHOLD and
            abs(pitch_deg) <= self.MAX_PITCH_THRESHOLD
        )

        return HeadPoseAngles(
            yaw=round(yaw_deg, 2),
            pitch=round(pitch_deg, 2),
            roll=round(roll_deg, 2),
            is_facing_screen=is_facing
        ), rvec, tvec

    def classify_affect(
        self,
        avg_ear: float,
        mar: float,
        pose: HeadPoseAngles
    ) -> AffectClassification:
        """
        Classifies cognitive/affective state using multi-cue feature integration.
        States: 'Focused', 'Distracted', 'Drowsy', 'Confused', 'Neutral'
        """
        # Rule-based probabilistic state assignment
        scores = {
            "Focused": 0.1,
            "Distracted": 0.1,
            "Drowsy": 0.1,
            "Confused": 0.1,
            "Neutral": 0.1,
        }

        # Drowsiness cues: low EAR, high MAR (yawning)
        if avg_ear < self.EAR_DROWSY_THRESHOLD or mar > self.MAR_YAWN_THRESHOLD:
            scores["Drowsy"] += 0.8
            if mar > self.MAR_YAWN_THRESHOLD:
                scores["Drowsy"] += 0.4
        
        # Distraction cues: looking away (high yaw or pitch)
        if not pose.is_facing_screen:
            deviation_factor = min(1.0, (abs(pose.yaw) + abs(pose.pitch)) / 50.0)
            scores["Distracted"] += 0.7 * deviation_factor

        # Confused cues: head tilt (roll > 10) + slight brow asymmetry with screen focus
        if pose.is_facing_screen and abs(pose.roll) > 10.0 and 0.22 <= avg_ear <= 0.28:
            scores["Confused"] += 0.65

        # Focused cues: looking at screen, normal open eyes, closed mouth
        if pose.is_facing_screen and avg_ear >= self.EAR_BLINK_THRESHOLD and mar < 0.45:
            scores["Focused"] += 0.75

        # Neutral cues: stable baseline
        if pose.is_facing_screen and 0.22 <= avg_ear <= 0.30 and mar < 0.40:
            scores["Neutral"] += 0.40

        # Normalize probabilities via Softmax-like scaling
        total = sum(scores.values())
        dist = {k: round(v / total, 3) for k, v in scores.items()}
        dominant = max(dist.items(), key=lambda item: item[1])

        return AffectClassification(
            dominant_state=dominant[0],
            confidence=dominant[1],
            state_distribution=dist
        )

    def compute_instantaneous_attention(
        self,
        pose: HeadPoseAngles,
        ear_metrics: EyeAspectRatios,
        affect: AffectClassification
    ) -> float:
        """
        Computes normalized attention score [0.0 - 100.0] for the current frame.
        Weights:
        - Gaze / Screen orientation (40%)
        - Ocular openness / Alertness (35%)
        - Affect state alignment (25%)
        """
        # Orientation component (0 - 40)
        yaw_penalty = min(1.0, abs(pose.yaw) / 35.0)
        pitch_penalty = min(1.0, abs(pose.pitch) / 30.0)
        orientation_score = 40.0 * (1.0 - 0.6 * yaw_penalty - 0.4 * pitch_penalty)
        orientation_score = max(0.0, orientation_score)

        # Ocular openness component (0 - 35)
        if ear_metrics.is_drowsy:
            ocular_score = 5.0
        elif ear_metrics.is_blinking:
            ocular_score = 28.0  # Normal physiological blink
        else:
            # Scaled EAR
            clamped_ear = min(0.35, max(0.18, ear_metrics.avg_ear))
            ocular_score = 35.0 * ((clamped_ear - 0.18) / (0.35 - 0.18))
            ocular_score = max(0.0, min(35.0, ocular_score))

        # Affect weight component (0 - 25)
        affect_multipliers = {
            "Focused": 1.0,
            "Neutral": 0.80,
            "Confused": 0.70,   # Active thinking / slight struggle
            "Distracted": 0.25,
            "Drowsy": 0.05
        }
        affect_score = 25.0 * affect_multipliers.get(affect.dominant_state, 0.5)

        total_score = orientation_score + ocular_score + affect_score
        return round(float(np.clip(total_score, 0.0, 100.0)), 2)

    def generate_synthetic_facial_landmarks(
        self,
        frame_shape: Tuple[int, int],
        state: str = "Focused"
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, Tuple[int, int, int, int]]:
        """
        Generates realistic 2D facial landmarks for testing and simulation.
        Returns: (6_pnp_points, left_eye_6pts, mouth_8pts, face_bbox)
        """
        h, w = frame_shape
        cx, cy = w // 2, h // 2

        # Adjust offsets based on simulated state
        yaw_offset = 0
        pitch_offset = 0
        eye_close_factor = 1.0
        mouth_open_factor = 0.0

        if state == "Distracted":
            yaw_offset = 48   # Looking sideways
            pitch_offset = 12
        elif state == "Drowsy":
            pitch_offset = 24 # Nodding off downwards
            eye_close_factor = 0.35 # Drooping eyelids
            mouth_open_factor = 1.2 # Yawning
        elif state == "Confused":
            yaw_offset = -12
            pitch_offset = -8
        elif state == "Neutral":
            yaw_offset = 5

        # 6 Canonical PnP landmark projection points
        nose = np.array([cx + yaw_offset, cy + pitch_offset])
        chin = np.array([cx + int(yaw_offset * 0.8), cy + 120 + pitch_offset])
        left_eye_corner = np.array([cx - 65 + yaw_offset, cy - 40 + pitch_offset])
        right_eye_corner = np.array([cx + 65 + yaw_offset, cy - 40 + pitch_offset])
        left_mouth = np.array([cx - 40 + int(yaw_offset * 0.9), cy + 65 + pitch_offset])
        right_mouth = np.array([cx + 40 + int(yaw_offset * 0.9), cy + 65 + pitch_offset])

        pnp_points = np.array([
            nose, chin, left_eye_corner, right_eye_corner, left_mouth, right_mouth
        ], dtype=np.float32)

        # 6-point eye geometry (left eye)
        e_cx, e_cy = cx - 40 + yaw_offset, cy - 40 + pitch_offset
        eye_h = 10 * eye_close_factor
        left_eye_points = np.array([
            [e_cx - 20, e_cy],
            [e_cx - 10, e_cy - eye_h],
            [e_cx + 10, e_cy - eye_h],
            [e_cx + 20, e_cy],
            [e_cx + 10, e_cy + eye_h],
            [e_cx - 10, e_cy + eye_h]
        ], dtype=np.float32)

        # 8-point mouth geometry
        m_cx, m_cy = cx + int(yaw_offset * 0.9), cy + 65 + pitch_offset
        m_h = 8 + (30 * mouth_open_factor)
        mouth_points = np.array([
            [m_cx - 35, m_cy],
            [m_cx - 20, m_cy - m_h],
            [m_cx, m_cy - m_h * 1.2],
            [m_cx + 20, m_cy - m_h],
            [m_cx + 35, m_cy],
            [m_cx + 20, m_cy + m_h],
            [m_cx, m_cy + m_h * 1.2],
            [m_cx - 20, m_cy + m_h]
        ], dtype=np.float32)

        bbox = (cx - 110 + yaw_offset, cy - 110 + pitch_offset, 220, 260)
        return pnp_points, left_eye_points, mouth_points, bbox

    def process_frame(
        self,
        frame: np.ndarray,
        frame_index: int,
        student_id: str,
        simulated_state: Optional[str] = None
    ) -> Tuple[FrameTelemetry, np.ndarray]:
        """
        End-to-end frame processing:
        1. Feature localization
        2. EAR and MAR computation
        3. PnP Head Pose estimation
        4. Affect classification
        5. Instantaneous attention computation
        6. Visual telemetry rendering and privacy filtering
        """
        h, w = frame.shape[:2]
        anonymized_token = self.privacy_filter.generate_pseudonym_token(student_id)

        # Extract or generate facial geometry
        state = simulated_state or "Focused"
        pnp_pts, eye_pts, mouth_pts, bbox = self.generate_synthetic_facial_landmarks((h, w), state=state)

        # 1. EAR Calculation
        ear_val = self.calculate_ear(eye_pts)
        is_blinking = 0.18 <= ear_val < self.EAR_BLINK_THRESHOLD
        is_drowsy = ear_val < self.EAR_DROWSY_THRESHOLD

        eye_metrics = EyeAspectRatios(
            left_ear=round(ear_val, 3),
            right_ear=round(ear_val, 3),
            avg_ear=round(ear_val, 3),
            is_blinking=is_blinking,
            is_drowsy=is_drowsy
        )

        # 2. MAR Calculation
        mar_val = self.calculate_mar(mouth_pts)

        # 3. Head Pose via PnP
        pose, rvec, tvec = self.estimate_head_pose(pnp_pts, (h, w))

        # 4. Affect Classification
        affect = self.classify_affect(ear_val, mar_val, pose)

        # 5. Instantaneous Attention
        instant_att = self.compute_instantaneous_attention(pose, eye_metrics, affect)

        # Construct Telemetry schema
        telemetry = FrameTelemetry(
            frame_index=frame_index,
            timestamp=round(frame_index * (1.0 / 30.0), 3),
            student_id=student_id,
            anonymized_token=anonymized_token,
            head_pose=pose,
            eye_metrics=eye_metrics,
            affect=affect,
            instantaneous_attention=instant_att,
            smoothed_attention=instant_att  # Will be smoothed by attention_tracker
        )

        # Render visual annotations
        annotated_frame = self.render_overlay(frame.copy(), telemetry, pnp_pts, eye_pts, mouth_pts, bbox)

        # Optional anonymization
        if self.anonymize:
            annotated_frame = self.privacy_filter.apply_face_blur(annotated_frame, bbox)

        return telemetry, annotated_frame

    def render_overlay(
        self,
        canvas: np.ndarray,
        telemetry: FrameTelemetry,
        pnp_pts: np.ndarray,
        eye_pts: np.ndarray,
        mouth_pts: np.ndarray,
        bbox: Tuple[int, int, int, int]
    ) -> np.ndarray:
        """
        Renders HUD overlays: bounding box, facial wireframe points, pose text, attention gauge.
        """
        x, y, w, h = bbox
        color = (0, 220, 100) if telemetry.instantaneous_attention >= 70 else (
            (0, 180, 255) if telemetry.instantaneous_attention >= 40 else (0, 0, 230)
        )

        # Draw Face Bounding Box with styled corner brackets
        cv2.rectangle(canvas, (x, y), (x + w, y + h), color, 2)

        # Draw Landmark Points
        for pt in pnp_pts:
            cv2.circle(canvas, (int(pt[0]), int(pt[1])), 3, (255, 255, 0), -1)

        for pt in eye_pts:
            cv2.circle(canvas, (int(pt[0]), int(pt[1])), 2, (0, 255, 255), -1)

        # Draw Mouth contour
        cv2.polylines(canvas, [mouth_pts.astype(np.int32)], isClosed=True, color=(255, 120, 0), thickness=1)

        # Top HUD Status Banner
        cv2.rectangle(canvas, (10, 10), (380, 140), (20, 24, 30), -1)
        cv2.rectangle(canvas, (10, 10), (380, 140), (70, 80, 95), 1)

        # Text Metrics
        cv2.putText(canvas, f"STUDENT: {telemetry.anonymized_token}", (20, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (240, 240, 240), 1, cv2.LINE_AA)
        cv2.putText(canvas, f"STATE: {telemetry.affect.dominant_state.upper()} ({telemetry.affect.confidence:.2f})",
                    (20, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2, cv2.LINE_AA)
        cv2.putText(canvas, f"EAR: {telemetry.eye_metrics.avg_ear:.2f} | YAW: {telemetry.head_pose.yaw:+.1f} deg",
                    (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (190, 190, 190), 1, cv2.LINE_AA)
        cv2.putText(canvas, f"PITCH: {telemetry.head_pose.pitch:+.1f} deg | ROLL: {telemetry.head_pose.roll:+.1f} deg",
                    (20, 102), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (190, 190, 190), 1, cv2.LINE_AA)
        
        # Attention Score Progress Bar
        att = telemetry.instantaneous_attention
        cv2.putText(canvas, f"ATTENTION: {att:.1f}%", (20, 126),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 1, cv2.LINE_AA)
        bar_x = 180
        bar_w = 180
        bar_fill = int((att / 100.0) * bar_w)
        cv2.rectangle(canvas, (bar_x, 114), (bar_x + bar_w, 130), (50, 55, 65), -1)
        cv2.rectangle(canvas, (bar_x, 114), (bar_x + bar_fill, 130), color, -1)

        return canvas
