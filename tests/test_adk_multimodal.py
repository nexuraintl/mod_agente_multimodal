#!/usr/bin/env python3
"""Test para verificar soporte multimodal en ADKClient"""
import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.adk_client import ADKClient

class TestADKMultimodal(unittest.TestCase):
    
    @patch('utils.adk_client.genai.Client')
    def test_diagnose_ticket_with_images(self, mock_genai_client):
        """Verifica que diagnose_ticket acepte y envíe imágenes al modelo."""
        
        # Setup mock
        mock_model = MagicMock()
        mock_client_instance = mock_genai_client.return_value
        mock_client_instance.models = mock_model
        
        mock_response = MagicMock()
        mock_response.text = '{"diagnostico": "Veo un error en la imagen", "type_id": 10}'
        mock_model.generate_content.return_value = mock_response

        # Initialize client
        # Env var needs to be mocked or present. Assuming load_dotenv runs in adk_client or env is set.
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "fake_key"}):
            client = ADKClient()
            
            # Dummy image data (bytes)
            dummy_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR...'
            
            # Simular un objeto imagen o un dict que representa la imagen
            # En nuestro diseño, pasaremos los bytes o un objeto PIL. 
            # Para simplificar la interfaz, asumiremos que pasamos un dict con 'mime_type' y 'data'
            images = [
                {'mime_type': 'image/png', 'data': dummy_image_data}
            ]
            
            ticket_text = "Tengo un problema, ver imagen."
            
            response = client.diagnose_ticket(ticket_text, images=images)
            
            # Verificaciones
            self.assertIn("Veo un error", response)
            
            # Verificar llamada al modelo
            mock_model.generate_content.assert_called_once()
            call_args = mock_model.generate_content.call_args
            contents = call_args[1]['contents']
            
            # El contenido debe ser la lista [prompt, image1]
            self.assertTrue(isinstance(contents, list), "Contents debe ser una lista cuando hay imágenes")
            self.assertEqual(len(contents), 2, "Debe haber 2 partes: Prompt texto e Imagen")
            
            # types.Part es un objeto, no un diccionario
            image_part = contents[1]
            self.assertEqual(image_part.inline_data.data, dummy_image_data)
            self.assertEqual(image_part.inline_data.mime_type, 'image/png')

if __name__ == '__main__':
    unittest.main()
