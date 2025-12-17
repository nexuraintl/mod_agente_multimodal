#!/usr/bin/env python3
"""Test de integración del flujo multimodal"""
import sys
import os
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.update_service import ZnunyService

class TestIntegrationMultimodal(unittest.TestCase):
    
    @patch('services.update_service.requests')
    def test_full_multimodal_flow(self, mock_requests):
        """
        Verifica que ZnunyService coordine correctamente:
        1. Obtención de texto
        2. Obtención de imágenes
        3. Llamada al Agente (con imágenes)
        4. Actualización del ticket
        """
        
        # Mocks
        service = ZnunyService()
        service._cached_session_id = "mock_session"
        
        # Mock methods to isolate orchestration logic
        service.get_ticket_latest_article = MagicMock(return_value="Problema visual")
        
        fake_images = [{'mime_type': 'image/png', 'data': b'fake', 'filename': 'a.png'}]
        service.get_ticket_attachments = MagicMock(return_value=fake_images)
        
        service.update_ticket = MagicMock(return_value={"ArticleID": 999})
        
        # Mock KB Service to avoid real DB/API calls
        service._kb_service = MagicMock()
        service._kb_service.get_or_create_store.return_value = "mock_store"
        service._kb_service.get_tool_config.return_value = []

        # Mock AgentService
        service._agent_service = MagicMock()
        service._agent_service.diagnose_ticket.return_value = {
            "type_id": 10,
            "diagnostico": "Diagnóstico final"
        }
        
        # Ejecutar
        result = service.diagnose_and_update_ticket(ticket_id=100, session_id="mock_session")
        
        # Verificaciones
        
        # 1. Se buscaron adjuntos?
        service.get_ticket_attachments.assert_called_once_with(100, "mock_session")
        
        # 2. Se llamó al agente con las imágenes?
        service._agent_service.diagnose_ticket.assert_called_once()
        args, kwargs = service._agent_service.diagnose_ticket.call_args
        self.assertEqual(kwargs['images'], fake_images)
        
        # 3. Se actualizó el ticket?
        service.update_ticket.assert_called_once()
        self.assertTrue(result['ok'])

if __name__ == '__main__':
    unittest.main()
