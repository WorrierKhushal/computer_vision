"""
Unit tests for Computer Vision Engine, EAR/MAR formulas, and Privacy Filter.
Author: Khushal Mahajan (24MIM10014)
"""
import unittest
import numpy as np
from core.vision_engine import ComputerVisionEngine
from core.privacy_filter import PrivacyPreservingFilter
from core.attention_tracker import AttentionTracker


class TestVisionEngine(unittest.TestCase):
    def setUp(self):
        self.vision_engine = ComputerVisionEngine(anonymize=False)
        self.privacy_filter = PrivacyPreservingFilter()

    def test_ear_calculation_open_and_closed_eye(self):
        """
        Validates EAR equation:
        EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
        """
        # Open eye coordinates
        open_eye = np.array([
            [0.0, 0.0],
            [10.0, 6.0],
            [20.0, 6.0],
            [30.0, 0.0],
            [20.0, -6.0],
            [10.0, -6.0]
        ])
        ear_open = self.vision_engine.calculate_ear(open_eye)
        self.assertGreater(ear_open, 0.25)

        # Closed eye coordinates (collapsed vertical distance)
        closed_eye = np.array([
            [0.0, 0.0],
            [10.0, 1.0],
            [20.0, 1.0],
            [30.0, 0.0],
            [20.0, -1.0],
            [10.0, -1.0]
        ])
        ear_closed = self.vision_engine.calculate_ear(closed_eye)
        self.assertLess(ear_closed, 0.15)

    def test_mar_calculation_normal_and_yawn(self):
        """
        Validates Mouth Aspect Ratio (MAR) yawn detector.
        """
        # Normal relaxed closed/slightly parted mouth
        normal_mouth = np.array([
            [0, 0], [10, 2], [20, 3], [30, 2],
            [40, 0], [30, -2], [20, -3], [10, -2]
        ], dtype=np.float32)
        mar_normal = self.vision_engine.calculate_mar(normal_mouth)
        self.assertLess(mar_normal, 0.40)

        # Wide open mouth (Yawn)
        yawn_mouth = np.array([
            [0, 0], [10, 22], [20, 26], [30, 22],
            [40, 0], [30, -22], [20, -26], [10, -22]
        ], dtype=np.float32)
        mar_yawn = self.vision_engine.calculate_mar(yawn_mouth)
        self.assertGreater(mar_yawn, 0.65)

    def test_pnp_head_pose_estimation(self):
        """
        Validates Perspective-n-Point orientation estimation.
        """
        front_points = np.array([
            [320.0, 240.0],   # Nose
            [320.0, 360.0],   # Chin
            [255.0, 180.0],   # Left eye
            [385.0, 180.0],   # Right eye
            [280.0, 290.0],   # Left mouth
            [360.0, 290.0],   # Right mouth
        ], dtype=np.float32)

        pose, _, _ = self.vision_engine.estimate_head_pose(front_points, (480, 640))
        self.assertLess(abs(pose.yaw), 20.0)
        self.assertLess(abs(pose.pitch), 20.0)
        self.assertTrue(pose.is_facing_screen)

    def test_privacy_pseudonymization(self):
        """
        Verifies cryptographic pseudonym token generation.
        """
        token1 = self.privacy_filter.generate_pseudonym_token("24MIM10014")
        token2 = self.privacy_filter.generate_pseudonym_token("24MIM10014")
        token3 = self.privacy_filter.generate_pseudonym_token("24MIM10002")

        self.assertTrue(token1.startswith("ANON-"))
        self.assertEqual(token1, token2)
        self.assertNotEqual(token1, token3)

    def test_temporal_attention_tracker(self):
        """
        Verifies EMA smoothing and fatigue accumulation.
        """
        tracker = AttentionTracker(student_id="24MIM10014", alpha_ema=0.25)
        engine = ComputerVisionEngine()
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)

        for i in range(20):
            telemetry, _ = engine.process_frame(dummy_frame, i, "24MIM10014", simulated_state="Focused")
            smoothed = tracker.update(telemetry)
            self.assertGreater(smoothed.smoothed_attention, 0.0)

        summary = tracker.get_session_summary()
        self.assertEqual(summary.frames_analyzed, 20)
        self.assertGreaterEqual(summary.mean_attention_score, 65.0)


if __name__ == "__main__":
    unittest.main()
