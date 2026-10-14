"""
Core modules for SmartVision-Ed.
Author: Khushal Mahajan (24MIM10014)
"""
from core.vision_engine import ComputerVisionEngine
from core.attention_tracker import AttentionTracker
from core.risk_analyzer import AcademicRiskAnalyzer
from core.privacy_filter import PrivacyPreservingFilter

__all__ = [
    "ComputerVisionEngine",
    "AttentionTracker",
    "AcademicRiskAnalyzer",
    "PrivacyPreservingFilter"
]
