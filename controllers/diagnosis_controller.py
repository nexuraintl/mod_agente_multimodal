# controllers/diagnosis_controller.py
"""Controller for the AI Diagnosis Service."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging

from models.diagnosis_models import DiagnosisRequest, DiagnosisResponse
from services.diagnosis_service import diagnosis_service

logger = logging.getLogger(__name__)

diagnosis_router = APIRouter(tags=["diagnosis"])


@diagnosis_router.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose(request: DiagnosisRequest) -> DiagnosisResponse:
    """
    Generate AI diagnosis for a design ticket.
    
    This endpoint receives ticket data (text and optional images) and returns
    an AI-generated diagnosis. Supports visual analysis of images with color
    annotations for block identification.
    
    **Consumed by:** agents_mod microservice
    
    **Type Classifications:**
    - 10: Incident (bug/error in existing UI)
    - 14: Request (modification to existing component)
    - 19: Requirement (new component/functionality)
    
    **Visual Analysis:**
    When images with color borders are provided, the AI identifies blocks:
    - Yellow (#FFF200) → bloqueEditor
    - Blue (#0023F5) → bloqueLayout  
    - Cyan (#00FFFF) → bloqueDynamic
    """
    logger.info(f"[/diagnose] Received request for ticket: {request.ticket_id or 'N/A'}")
    
    try:
        result = diagnosis_service.diagnose(request)
        
        if result.status == "error":
            logger.error(f"[/diagnose] Diagnosis failed: {result.error}")
        else:
            logger.info(f"[/diagnose] Diagnosis completed. TypeID: {result.type_id}")
        
        return result
        
    except Exception as e:
        logger.error(f"[/diagnose] Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@diagnosis_router.get("/health")
async def health():
    """
    Health check endpoint.
    
    Returns service status for load balancers and monitoring.
    """
    return {
        "status": "healthy",
        "service": "ai-diagnosis-service",
        "version": "2.0.0"
    }


@diagnosis_router.get("/")
async def root():
    """
    Root endpoint with service information.
    """
    return {
        "service": "AI Diagnosis Service",
        "description": "Pure AI diagnosis service for design tickets",
        "endpoints": {
            "POST /diagnose": "Generate AI diagnosis for a ticket",
            "GET /health": "Health check",
            "GET /docs": "OpenAPI documentation"
        },
        "consumed_by": "agents_mod"
    }
