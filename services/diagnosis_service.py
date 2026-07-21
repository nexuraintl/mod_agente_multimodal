# services/diagnosis_service.py
"""Pure AI Diagnosis Service for design tickets."""

import base64
import time
import logging
import json
from typing import Optional

from .agent_service import AgentService
from .knowledge_base_service import KnowledgeBaseService
from models.diagnosis_models import DiagnosisRequest, DiagnosisResponse

logger = logging.getLogger(__name__)


class DiagnosisService:
    """
    Pure AI diagnosis service for design tickets.
    Does NOT interact with Znuny - only processes tickets and returns diagnosis.
    Consumed by agents_mod microservice.
    """

    def __init__(self):
        self._agent_service: Optional[AgentService] = None
        self._kb_service: Optional[KnowledgeBaseService] = None

    @property
    def agent_service(self) -> AgentService:
        """Lazy initialization of AgentService."""
        if self._agent_service is None:
            self._agent_service = AgentService()
        return self._agent_service


    def _decode_images(self, images: list) -> list:
        """
        Decode base64 images to bytes for AI processing.
        
        Args:
            images: List of ImageData objects with base64 encoded data
            
        Returns:
            List of dicts with decoded image bytes
        """
        decoded = []
        for img in images:
            try:
                decoded_data = base64.b64decode(img.data)
                decoded.append({
                    "mime_type": img.mime_type,
                    "data": decoded_data,
                    "filename": img.filename or "image.png"
                })
            except Exception as e:
                logger.warning(f"Failed to decode image {img.filename}: {e}")
        return decoded


    def diagnose(self, request: DiagnosisRequest) -> DiagnosisResponse:
        """
        Generate AI diagnosis for a design ticket.
        
        Args:
            request: DiagnosisRequest with ticket_text and optional images
            
        Returns:
            DiagnosisResponse with diagnosis and type_id
        """
        start_time = time.time()
        
        try:
            # 1. Validate input
            if not request.ticket_text.strip():
                return DiagnosisResponse(
                    status="error",
                    error="Error: No se recibió texto",
                    diagnosis= "",
                    type_id=14,
                    processing_time_ms=(time.time() - start_time) * 1000
                )

            logger.info(f"📋 Processing diagnosis for ticket: {request.ticket_id or 'N/A'}")
            logger.info(f"   Text length: {len(request.ticket_text)} chars")
            logger.info(f"   Images: {len(request.images) if request.images else 0}")

            # 2. Decode images if present
            decoded_images = []
            if request.images:
                for img in request.images:
                    try:
                        decoded_images.append({
                            "mime_type": img.mime_type,
                            "data": base64.b64decode(img.data)
                        })
                    except Exception as e:
                        logger.warning(f"Error decodificando imagen: {e}")
        
            

            # 3. Call AI for diagnosis
            logger.info("🤖 Generating diagnosis with AI...")
            response_data = self.agent_service.diagnose_ticket(
                ticket_text=request.ticket_text,
                tool_config=None,
                images=decoded_images
            )

            # 4. Process response
            final_diagnosis_text = ""
            detected_blocks =[]
            type_id = 14 #Default: Requerimiento
            if isinstance(response_data, dict):
                # Raw string response
                type_id = response_data.get("type_id", 14)
                raw_diag = response_data.get("diagnostico", "")

                # Lógica de extracción de bloques JSON
                if isinstance(raw_diag, str) and (raw_diag.strip().startswith("[") or raw_diag.strip().startswith("{")):
                    try:
                        # Intentamos extraer bloques si la IA mandó JSON
                        parsed = json.loads(raw_diag)
                        if isinstance(parsed, list):
                            detected_blocks = parsed
                            final_diagnosis_text = f"Se detectaron {len(detected_blocks)} bloques técnicos para procesar."
                        else:
                            detected_blocks = [parsed]
                            final_diagnosis_text = "Se detectó un bloque técnico."
                    except:
                        final_diagnosis_text = raw_diag
                else:
                    final_diagnosis_text = raw_diag
            else:
                final_diagnosis_text = str(response_data)

            processing_time = (time.time() - start_time) * 1000
            

        
            # 6. Validate diagnosis
            if not final_diagnosis_text:
                return DiagnosisResponse(
                    status="error",
                    error="AI returned empty diagnosis",
                    processing_time_ms=(time.time() - start_time) * 1000
                )

            processing_time = (time.time() - start_time) * 1000
            logger.info(f"✅ Diagnosis completed in {processing_time:.2f}ms. TypeID: {type_id}")
            
            return DiagnosisResponse(
                status="ok",
                type_id=type_id,
                diagnosis=final_diagnosis_text, # Texto para la nota de Znuny
                blocks=detected_blocks,        # JSON para el sistema de diseño
                processing_time_ms=processing_time
            )


        except Exception as e:
            logger.error(f"❌ Diagnosis failed: {e}", exc_info=True)
            return DiagnosisResponse(
                status="error",
                error=str(e),
                diagnosis="Error interno en el especialista multimodal",
                type_id=14,
                processing_time_ms=(time.time() - start_time) * 1000
            )


# Singleton instance
diagnosis_service = DiagnosisService()
