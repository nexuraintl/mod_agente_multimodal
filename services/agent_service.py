# services/agent_service.py

import json
import logging
from typing import Union, Dict, Any, Optional
from utils.adk_client import ADKClient

logger = logging.getLogger(__name__)

class AgentService:
    def __init__(self):
        self.adk_client = ADKClient()

    def diagnose_ticket(self, ticket_text: str, tool_config=None, images=None) -> Union[str, Dict[str, Optional[str]]]:
        """
        Calls the model, receives a JSON string, parses it, and returns the formatted
        diagnosis text for the Znuny article.
        """
        response_text = self.adk_client.diagnose_ticket(ticket_text, tool_config, images)
        
        if not response_text:
            logger.error("❌ El modelo de IA no devolvió ninguna respuesta.")
            return {"diagnostico": "Error: El modelo no respondió.", "type_id": 14}

        # Try to parse the JSON returned by the IA
        try:

            data = json.loads(response_text.strip())
            diagnostico = data.get("diagnostico") or data.get("diagnosis")
            type_id = data.get("type_id", 14)

            if not diagnostico:
                # Caso especial: A veces la IA devuelve directamente el array de bloques en el root
                if isinstance(data, list):
                    return {
                        "type_id": 14,
                        "diagnostico": json.dumps(data) # Lo pasamos como string para que el Service lo procese
                    }
                return {"diagnostico": "La IA no generó un diagnóstico válido.", "type_id": 14}

            return {
                "type_id": int(type_id) if type_id else 14,
                "diagnostico": diagnostico
            }

        except json.JSONDecodeError:
            # Fallback en caso de que la IA ignore el formato JSON (poco probable en 2.0 Flash)
            logger.warning("⚠️ La respuesta de la IA no es un JSON válido. Intentando rescate de texto.")
            return {
                "type_id": 14,
                "diagnostico": response_text.strip()
            }