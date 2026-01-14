# models/__init__.py
"""Models package for AI Diagnosis Service."""

from .diagnosis_models import DiagnosisRequest, DiagnosisResponse, ImageData

__all__ = ["DiagnosisRequest", "DiagnosisResponse", "ImageData"]
