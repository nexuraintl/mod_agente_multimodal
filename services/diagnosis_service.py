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

    @property
    def kb_service(self) -> KnowledgeBaseService:
        """Lazy initialization of KnowledgeBaseService."""
        if self._kb_service is None:
            self._kb_service = KnowledgeBaseService()
        return self._kb_service

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

    def _get_rag_tool_config(self):
        """
        Get RAG tool configuration for Knowledge Base search.
        
        Returns:
            Tool config or None if RAG fails
        """
        try:
            store_name = self.kb_service.get_or_create_store(display_name="Znuny_Tickets_KB")
            if store_name:
                tool_config = self.kb_service.get_tool_config(store_name)
                logger.info(f"✅ RAG configured with Store: {store_name}")
                return tool_config
            else:
                logger.warning("⚠️ Failed to get Store Name for RAG")
                return None
        except Exception as e:
            logger.error(f"❌ Error configuring RAG: {e}")
            return None

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
            if not request.ticket_text or not request.ticket_text.strip():
                return DiagnosisResponse(
                    status="error",
                    error="ticket_text is required and cannot be empty",
                    processing_time_ms=(time.time() - start_time) * 1000
                )

            logger.info(f"📋 Processing diagnosis for ticket: {request.ticket_id or 'N/A'}")
            logger.info(f"   Text length: {len(request.ticket_text)} chars")
            logger.info(f"   Images: {len(request.images) if request.images else 0}")

            # 2. Decode images if present
            images = []
            if request.images:
                images = self._decode_images(request.images)
                logger.info(f"📸 Decoded {len(images)} images for visual analysis")

            # 3. Get RAG tool config if enabled
            tool_config = None
            if request.use_rag:
                tool_config = self._get_rag_tool_config()

            # 4. Call AI for diagnosis
            logger.info("🤖 Generating diagnosis with AI...")
            response_data = self.agent_service.diagnose_ticket(
                ticket_text=request.ticket_text,
                tool_config=tool_config,
                images=images
            )

            # 5. Process response
            if isinstance(response_data, str):
                # Raw string response
                type_id = None
                diagnosis = response_data
            else:
                # Dict response with type_id and diagnostico
                type_id = response_data.get("type_id")
                diagnosis = response_data.get("diagnostico")

            # 6. Validate diagnosis
            if not diagnosis:
                return DiagnosisResponse(
                    status="error",
                    error="AI returned empty diagnosis",
                    processing_time_ms=(time.time() - start_time) * 1000
                )

            # 7. Try to parse diagnosis if it's a JSON string (for visual analysis blocks)
            if isinstance(diagnosis, str):
                try:
                    # Check if it's a JSON array (visual analysis result)
                    cleaned = diagnosis.strip()
                    if cleaned.startswith("["):
                        diagnosis = json.loads(cleaned)
                        logger.info(f"📦 Parsed {len(diagnosis)} visual blocks from diagnosis")
                except json.JSONDecodeError:
                    # Keep as string (HTML/code response)
                    pass

            processing_time = (time.time() - start_time) * 1000
            logger.info(f"✅ Diagnosis completed in {processing_time:.2f}ms. TypeID: {type_id}")

            return DiagnosisResponse(
                status="ok",
                type_id=type_id,
                diagnosis=diagnosis,
                processing_time_ms=processing_time
            )

        except Exception as e:
            logger.error(f"❌ Diagnosis failed: {e}", exc_info=True)
            return DiagnosisResponse(
                status="error",
                error=str(e),
                processing_time_ms=(time.time() - start_time) * 1000
            )


# Singleton instance
diagnosis_service = DiagnosisService()
