from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import datetime
import json
import os
import logging
from services.update_service import ZnunyService
from models.webhook_models import WebhookResponse

# Configure logging
logger = logging.getLogger(__name__)

agent_router = APIRouter(tags=["webhooks"])

# Instantiate service
znuny_service = ZnunyService()

# --- Helper Functions ---

def _get_ticket_id(payload_json: dict, query_params: dict) -> str | None:
    """
    Extracts TicketID from various possible locations in the payload or query parameters.
    Prioritizes Query Params -> JSON Body (Event -> Ticket -> Data).
    """
    # 1. Try Query Params
    if ticket_id := query_params.get("TicketID"):
        return str(ticket_id)

    # 2. Try JSON Body Structure
    if not isinstance(payload_json, dict):
        return None

    # Common structures for Znuny/OTRS webhooks
    possible_paths = [
        ["TicketID"],
        ["Event", "TicketID"],
        ["Ticket", "TicketID"],
        ["Data", "Event", "TicketID"],
        ["Article", "TicketID"]
    ]

    for path in possible_paths:
        value = payload_json
        for key in path:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                value = None
                break
        if value:
            return str(value)

    return None

def _log_payload(payload: dict):
    """Logs the received payload to a file for audit purposes."""
    try:
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
        os.makedirs(logs_dir, exist_ok=True)
        log_file = os.path.join(logs_dir, "znuny_requests.log")
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n\n")
            
    except Exception as e:
        logger.error(f"Failed to write to audit log: {e}")

# --- Endpoints ---

@agent_router.api_route("/znuny-webhook", methods=["GET", "POST", "PUT"], response_model=WebhookResponse)
async def znuny_webhook(request: Request):
    """
    Receives webhooks from Znuny, logs the request, and triggers a ticket update/diagnosis.
    """
    # 1. Parse Request
    try:
        body_json = None
        form_data = None
        raw_body_str = None
        
        content_type = request.headers.get("content-type", "")
        
        if "application/json" in content_type:
            body_json = await request.json()
        elif "application/x-www-form-urlencoded" in content_type:
            form = await request.form()
            form_data = dict(form)
        else:
            raw = await request.body()
            raw_body_str = raw.decode("utf-8", errors="ignore")

    except Exception as e:
        logger.warning(f"Could not parse request body: {e}")
        # Continue execution to allow debugging with partial data
    
    # Construct complete payload object for logging
    payload = {
        "time": datetime.datetime.utcnow().isoformat() + "Z",
        "method": request.method,
        "headers": dict(request.headers),
        "args": dict(request.query_params),
        "json": body_json,
        "form": form_data,
        "raw_body": raw_body_str,
    }

    logger.info(f"Payload received: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    
    # 2. Audit Log
    _log_payload(payload)

    # 3. Extract TicketID
    ticket_id = _get_ticket_id(payload_json=body_json or {}, query_params=payload["args"])

    if not ticket_id:
        error_msg = "No TicketID found in payload (checked QueryParams and JSON body)"
        logger.error(error_msg)
        raise HTTPException(status_code=400, detail=error_msg)

    # 4. Session & Business Logic
    try:
        session_id = znuny_service.get_or_create_session_id()
        logger.info(f"[Webhook] ✅ SessionID obtained: {session_id}")
        
        logger.info(f"[Webhook] Processing ticket {ticket_id}...")
        result = znuny_service.diagnose_and_update_ticket(
            ticket_id=int(ticket_id),
            session_id=session_id,
            data=body_json
        )
        logger.info(f"[Webhook] Update for ticket {ticket_id} completed.")
        
        return WebhookResponse(
            status="ok", 
            ticket_id=str(ticket_id),
            diagnosis=result
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Webhook] Critical Error processing ticket {ticket_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")