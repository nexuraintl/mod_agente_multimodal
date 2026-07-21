# models/diagnosis_models.py
"""Pydantic models for the AI Diagnosis Service."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union


class ImageData(BaseModel):
    """Image data for visual analysis."""
    data: str = Field(..., description="Base64 encoded image data")
    mime_type: str = Field(default="image/png", description="MIME type of the image")
    filename: Optional[str] = Field(default=None, description="Original filename")


class DiagnosisRequest(BaseModel):
    """Request payload for the /diagnose endpoint."""
    ticket_id: Optional[str] = Field(default=None, description="Ticket ID for traceability")
    ticket_text: str = Field(..., description="Ticket content/body to diagnose")
    images: Optional[List[ImageData]] = Field(default_factory=list, description="Attached images for visual analysis")
    entity: Optional[str] = Field(default=None, description="Client/entity identifier")
    use_rag: bool = Field(default=True, description="Use Knowledge Base (RAG)")


class DiagnosisResponse(BaseModel):
    """Response from the /diagnose endpoint."""
    status: str = Field(..., description="'ok' or 'error'")
    type_id: Optional[int] = Field(default=None, description="Ticket classification: 10=Incident, 14=Request, 19=Requirement")
    diagnosis: str = Field(..., description="Explicación textual del diagnóstico")
    blocks: Optional[List[Dict[str, Any]]] = Field(default=None, description="Configuración técnica de bloques detectados")
    requires_visual: bool = Field(default=True) # Siempre true en este microservicio
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    processing_time_ms: Optional[float] = Field(default=None, description="Processing time in milliseconds")
    error: Optional[str] = Field(default=None, description="Error message if status='error'")
