"""
Temporal Attention Tracker & Session Aggregator for SmartVision-Ed.
Implements:
1. Exponential Moving Average (EMA) filtering for noise reduction
2. Consecutive-frame state machine for drowsiness & distraction episode detection
3. Blink rate frequency tracking
4. Session-level attention summarization and fatigue index calculation

Author: Khushal Mahajan (24MIM10014)
"""
from typing import List, Optional
from collections import deque
import numpy as np
from models.data_schemas import FrameTelemetry, SessionAttentionMetrics


class AttentionTracker:
    """
    Maintains temporal state for a student throughout an academic lecture or study session.
    """
    def __init__(
        self,
        student_id: str,
        session_id: str = "SESSION_DEFAULT",
        alpha_ema: float = 0.25,
        drowsy_frame_threshold: int = 14,
        distract_frame_threshold: int = 20
    ):
        self.student_id = student_id
        self.session_id = session_id
        self.alpha_ema = alpha_ema
        self.drowsy_frame_threshold = drowsy_frame_threshold
        self.distract_frame_threshold = distract_frame_threshold

        # Running temporal states
        self.current_smoothed_attention: Optional[float] = None
        self.consecutive_drowsy_frames = 0
        self.consecutive_distracted_frames = 0
        self.drowsiness_alerts_triggered = 0
        self.distraction_episodes_triggered = 0

        # Recent sliding buffers
        self.history_raw: deque = deque(maxlen=300)
        self.history_smoothed: deque = deque(maxlen=300)
        self.blink_timestamps: deque = deque(maxlen=100)

        # Session accumulator
        self.total_frames = 0
        self.focused_frames = 0
        self.frame_records: List[FrameTelemetry] = []

    def update(self, telemetry: FrameTelemetry) -> FrameTelemetry:
        """
        Updates temporal state with the latest frame telemetry.
        Applies EMA filter and updates state-event counters.
        """
        self.total_frames += 1
        raw_val = telemetry.instantaneous_attention

        # EMA filter
        if self.current_smoothed_attention is None:
            self.current_smoothed_attention = raw_val
        else:
            self.current_smoothed_attention = (
                self.alpha_ema * raw_val + (1.0 - self.alpha_ema) * self.current_smoothed_attention
            )

        telemetry.smoothed_attention = round(float(self.current_smoothed_attention), 2)
        self.history_raw.append(raw_val)
        self.history_smoothed.append(telemetry.smoothed_attention)

        # Focus classification threshold
        if telemetry.smoothed_attention >= 65.0:
            self.focused_frames += 1

        # Drowsiness detection state machine
        if telemetry.eye_metrics.is_drowsy:
            self.consecutive_drowsy_frames += 1
            if self.consecutive_drowsy_frames == self.drowsy_frame_threshold:
                self.drowsiness_alerts_triggered += 1
        else:
            self.consecutive_drowsy_frames = 0

        # Distraction detection state machine
        if not telemetry.head_pose.is_facing_screen:
            self.consecutive_distracted_frames += 1
            if self.consecutive_distracted_frames == self.distract_frame_threshold:
                self.distraction_episodes_triggered += 1
        else:
            self.consecutive_distracted_frames = 0

        # Blink tracking
        if telemetry.eye_metrics.is_blinking:
            self.blink_timestamps.append(telemetry.timestamp)

        self.frame_records.append(telemetry)
        return telemetry

    def calculate_fatigue_index(self) -> float:
        """
        Calculates Fatigue Index [0.0 - 100.0] based on drowsiness frequency,
        blink irregularity, and downward trend in attention over time.
        """
        if not self.history_smoothed:
            return 0.0

        # Component 1: Drowsiness event penalty (up to 45 pts)
        drowsy_penalty = min(45.0, self.drowsiness_alerts_triggered * 15.0)

        # Component 2: Attention slope / decay (up to 30 pts)
        if len(self.history_smoothed) >= 30:
            recent_avg = np.mean(list(self.history_smoothed)[-15:])
            early_avg = np.mean(list(self.history_smoothed)[:15])
            decay = max(0.0, float(early_avg - recent_avg))
            decay_penalty = min(30.0, decay * 1.5)
        else:
            decay_penalty = 0.0

        # Component 3: Overall low average attention (up to 25 pts)
        overall_mean = float(np.mean(list(self.history_smoothed)))
        mean_penalty = max(0.0, 25.0 * (1.0 - (overall_mean / 100.0)))

        fatigue = drowsy_penalty + decay_penalty + mean_penalty
        return round(float(np.clip(fatigue, 0.0, 100.0)), 2)

    def get_session_summary(self) -> SessionAttentionMetrics:
        """
        Compiles aggregate metrics for the session.
        """
        if self.total_frames == 0:
            return SessionAttentionMetrics(
                student_id=self.student_id,
                session_id=self.session_id,
                duration_seconds=0.0,
                frames_analyzed=0,
                mean_attention_score=0.0,
                focus_time_percentage=0.0,
                distraction_event_count=0,
                drowsiness_alert_count=0,
                fatigue_index=0.0
            )

        duration = self.total_frames * (1.0 / 30.0)
        mean_att = float(np.mean(list(self.history_smoothed))) if self.history_smoothed else 0.0
        focus_pct = (self.focused_frames / self.total_frames) * 100.0
        fatigue = self.calculate_fatigue_index()

        return SessionAttentionMetrics(
            student_id=self.student_id,
            session_id=self.session_id,
            duration_seconds=round(duration, 2),
            frames_analyzed=self.total_frames,
            mean_attention_score=round(mean_att, 2),
            focus_time_percentage=round(focus_pct, 2),
            distraction_event_count=self.distraction_episodes_triggered,
            drowsiness_alert_count=self.drowsiness_alerts_triggered,
            fatigue_index=fatigue
        )
