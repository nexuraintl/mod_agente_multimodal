#!/usr/bin/env python3
"""Test para verificar extracción de adjuntos en ZnunyService"""
import sys
import os
import unittest
import base64
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.update_service import ZnunyService

class TestZnunyAttachments(unittest.TestCase):
    
    @patch('services.update_service.requests.get')
    def test_get_ticket_attachments_images_only(self, mock_get):
        """Verifica que se extraigan solo imágenes válidas de los adjuntos."""
        
        # Mock de la respuesta de Znuny
        # Estructura típica: Ticket -> Article (list) -> Attachment (list)
        
        # Datos de prueba
        image_content = b'fake_image_data'
        image_b64 = base64.b64encode(image_content).decode('utf-8')
        
        mock_response = {
            "Ticket": [
                {
                    "TicketID": 123,
                    "Article": [
                        {
                            "ArticleID": 1,
                            "Body": "Texto del ticket",
                            "Attachment": [
                                {
                                    "Content": image_b64,
                                    "ContentType": "image/png",
                                    "Filename": "captura.png",
                                    "FileID": 101,
                                    "Disposition": "inline"
                                },
                                {
                                    "Content": "base64_pdf_data...",
                                    "ContentType": "application/pdf",
                                    "Filename": "doc.pdf",
                                    "FileID": 102
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        # Instanciar servicio (mockeando vars de entorno si es necesario)
        with patch.dict(os.environ, {
            "ZNUNY_BASE_API": "http://mock-znuny", 
            "ZNUNY_USERNAME": "u", 
            "ZNUNY_PASSWORD": "p"
        }):
            service = ZnunyService()
            # Inyectar session_id para evitar llamada a login
            service._cached_session_id = "mock_session"
            
            # Llamar al método (que aún no existe)
            attachments = service.get_ticket_attachments(ticket_id=123, session_id="mock_session")
            
            self.assertEqual(len(attachments), 1, "Debería haber encontrado 1 adjunto válido (la imagen)")
            
            img = attachments[0]
            self.assertEqual(img['mime_type'], "image/png")
            self.assertEqual(img['data'], image_content)
            self.assertEqual(img['filename'], "captura.png")

if __name__ == '__main__':
    unittest.main()
