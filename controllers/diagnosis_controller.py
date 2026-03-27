# controllers/diagnosis_controller.py
"""Controller for the AI Diagnosis Service."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging

from models.diagnosis_models import DiagnosisRequest, DiagnosisResponse
from services.diagnosis_service import diagnosis_service

logger = logging.getLogger(__name__)

diagnosis_router = APIRouter(tags=["AI Multimodal Diagnosis"])


@diagnosis_router.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose(request: DiagnosisRequest):
    """
    Genera un diagnóstico de IA para tickets de diseño o errores visuales.
    
    Identificación de bloques por colores:
    - Amarillo (#FFF200) -> bloqueEditor
    - Azul (#0023F5) -> bloqueLayout
    - Cian (#00FFFF) -> bloqueDynamic
    """
    ticket_log = f"Ticket: {request.ticket_id}" if request.ticket_id else "Contenido Directo"
    logger.info(f"[MULTIMODAL] Iniciando análisis visual para {ticket_log}")
    
    try:
        result = diagnosis_service.diagnose(request)
        
        if result.status == "error":
            logger.error(f"❌ Error en diagnóstico visual: {result.error}")
        else:
            logger.info(f"✅ Análisis completado. Tipo sugerido: {result.type_id}")
        
        return result
        
    except Exception as e:
        logger.error(f"💥 Error inesperado en el controlador multimodal: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno en Multimodal Service: {str(e)}")


@diagnosis_router.get("/health")
async def health():
    """
    Health check endpoint.
    
    Returns service status for load balancers and monitoring.
    """
    return {
        "status": "healthy",
        "service": "ai-multimodal-service",
        "version": "2.0.0",
        "capabilities": ["vision", "block_detection", "ui_ux_analysis"]
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
