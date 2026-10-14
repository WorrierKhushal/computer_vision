"""
Privacy Filter and De-identification Module for SmartVision-Ed.
Ensures student identity protection and compliance with academic data protection standards.
Author: Khushal Mahajan (24MIM10014)
"""
import hashlib
import numpy as np
import cv2
from typing import Tuple, Optional


class PrivacyPreservingFilter:
    """
    Applies real-time facial anonymization and pseudonymization.
    Generates cryptographic pseudonyms to track session metrics without exposing student PII.
    """
    def __init__(self, salt: str = "VIT_24MIM10014_SALT_2026"):
        self.salt = salt

    def generate_pseudonym_token(self, student_id: str) -> str:
        """
        Generates a salted SHA-256 hash token for student privacy.
        """
        combined = f"{self.salt}_{student_id}".encode("utf-8")
        token = hashlib.sha256(combined).hexdigest()[:12].upper()
        return f"ANON-{token}"

    def apply_face_blur(self, frame: np.ndarray, bbox: Tuple[int, int, int, int], blur_kernel: int = 45) -> np.ndarray:
        """
        Blurs facial region in the video frame to prevent visual identification.
        bbox: (x, y, w, h)
        """
        anonymized = frame.copy()
        x, y, w, h = bbox
        h_frame, w_frame = frame.shape[:2]
        
        # Clip coordinates within image boundary
        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(w_frame, x + w)
        y2 = min(h_frame, y + h)

        if x2 > x1 and y2 > y1:
            # Ensure kernel size is odd
            ksize = blur_kernel if blur_kernel % 2 == 1 else blur_kernel + 1
            face_roi = anonymized[y1:y2, x1:x2]
            blurred_roi = cv2.GaussianBlur(face_roi, (ksize, ksize), 30)
            anonymized[y1:y2, x1:x2] = blurred_roi

        return anonymized

    def apply_pixelation(self, frame: np.ndarray, bbox: Tuple[int, int, int, int], pixel_blocks: int = 14) -> np.ndarray:
        """
        Applies mosaic/pixelation to face bounding box.
        """
        anonymized = frame.copy()
        x, y, w, h = bbox
        h_frame, w_frame = frame.shape[:2]
        
        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(w_frame, x + w)
        y2 = min(h_frame, y + h)

        if x2 > x1 and y2 > y1:
            face_roi = anonymized[y1:y2, x1:x2]
            roi_h, roi_w = face_roi.shape[:2]
            
            # Downscale and upscale to achieve mosaic effect
            small = cv2.resize(face_roi, (pixel_blocks, pixel_blocks), interpolation=cv2.INTER_LINEAR)
            pixelated = cv2.resize(small, (roi_w, roi_h), interpolation=cv2.INTER_NEAREST)
            anonymized[y1:y2, x1:x2] = pixelated

        return anonymized
