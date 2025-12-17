"""Pydantic models for webhook validation and responses."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any


class TicketData(BaseModel):
    """Ticket information from Znuny."""
    TicketID: Optional[int] = None
    TicketNumber: Optional[str] = None
    Title: Optional[str] = None
    State: Optional[str] = None
    Priority: Optional[str] = None
    Queue: Optional[str] = None


class EventData(BaseModel):
    """Event information from Znuny."""
    TicketID: Optional[str] = None
    Event: Optional[str] = None


class WebhookPayload(BaseModel):
    """Znuny webhook payload structure."""
    model_config = ConfigDict(extra="allow")  # Allow additional fields
    
    Data: Optional[Dict[str, Any]] = None
    Ticket: Optional[TicketData] = None
    Event: Optional[EventData] = None
    TicketID: Optional[int] = None


class WebhookResponse(BaseModel):
    """Standard webhook response."""
    status: str = Field(..., description="Status of the webhook processing")
    ticket_id: Optional[str] = Field(None, description="Processed ticket ID")
    message: Optional[str] = Field(None, description="Additional message")
    diagnosis: Optional[Dict[str, Any]] = Field(None, description="Diagnosis data returned by the agent")
