"""
Unit tests for Multi-Modal Academic Risk Engine and CAVS Scoring.
Author: Khushal Mahajan (24MIM10014)
"""
import unittest
from core.risk_analyzer import AcademicRiskAnalyzer


class TestRiskAnalyzer(unittest.TestCase):
    def setUp(self):
        self.risk_analyzer = AcademicRiskAnalyzer()

    def test_cavs_calculation(self):
        """
        Validates CAVS formula:
        CAVS = 100 - [0.30*vis + 0.25*att + 0.25*int + 0.20*lms]
        """
        cavs_perfect = self.risk_analyzer.calculate_cavs(
            attendance=100.0,
            internal_marks=100.0,
            lms_score=100.0,
            visual_attention=100.0
        )
        self.assertEqual(cavs_perfect, 0.0)

        cavs_zero = self.risk_analyzer.calculate_cavs(
            attendance=0.0,
            internal_marks=0.0,
            lms_score=0.0,
            visual_attention=0.0
        )
        self.assertEqual(cavs_zero, 100.0)

        cavs_mid = self.risk_analyzer.calculate_cavs(
            attendance=80.0,
            internal_marks=80.0,
            lms_score=80.0,
            visual_attention=80.0
        )
        self.assertEqual(round(cavs_mid, 1), 20.0)

    def test_evaluate_student_critical_attendance_debarment(self):
        """
        Students with attendance < 75% must be classified as 'Critical Early Warning' regardless of marks.
        """
        profile = self.risk_analyzer.evaluate_student(
            student_id="24MIM10023",
            student_name="Test Student",
            attendance=68.0,
            internal_marks=85.0,
            lms_score=80.0,
            visual_attention=80.0
        )
        self.assertEqual(profile.risk_category, "Critical Early Warning")
        self.assertTrue(profile.early_dropout_flag)
        self.assertTrue(any("75% debarment" in f for f in profile.contributing_factors))

    def test_evaluate_student_high_achiever(self):
        """
        Validates evaluation of top-performing student (Khushal Mahajan).
        """
        profile = self.risk_analyzer.evaluate_student(
            student_id="24MIM10014",
            student_name="Khushal Mahajan",
            attendance=94.5,
            internal_marks=92.0,
            lms_score=88.5,
            visual_attention=86.4
        )
        self.assertEqual(profile.risk_category, "Low Risk")
        self.assertFalse(profile.early_dropout_flag)
        self.assertLess(profile.composite_vulnerability_score, 20.0)


if __name__ == "__main__":
    unittest.main()
