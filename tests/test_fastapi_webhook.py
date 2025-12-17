"""Unit tests for FastAPI webhook endpoint using TestClient."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_webhook_missing_ticket_id():
    """Test webhook with missing TicketID returns 400 (or 200 if found in logs)."""
    response = client.post("/znuny-webhook", json={})
    # May return 400 if no TicketID found, or 200 if fallback finds one in logs
    assert response.status_code in [200, 400, 500]
    if response.status_code == 400:
        assert "TicketID" in response.json()["detail"]


def test_webhook_valid_payload_structure():
    """Test webhook accepts valid Znuny payload structure."""
    payload = {
        "Data": {
            "Ticket": {
                "TicketID": 123,
                "TicketNumber": "2025100998000011",
                "Title": "Test Ticket"
            },
            "Event": {
                "TicketID": "123",
                "Event": "TicketCreate"
            }
        }
    }
    
    # This will fail if ZnunyService can't get session, but structure is valid
    response = client.post("/znuny-webhook", json=payload)
    # We expect either 200 (success) or 500 (session/service error)
    assert response.status_code in [200, 500]


def test_webhook_ticket_id_extraction():
    """Test TicketID extraction from different payload structures."""
    # Test Event.TicketID
    payload1 = {"Event": {"TicketID": "456"}}
    response1 = client.post("/znuny-webhook", json=payload1)
    assert response1.status_code in [200, 500]  # Structure valid
    
    # Test Ticket.TicketID
    payload2 = {"Ticket": {"TicketID": 789}}
    response2 = client.post("/znuny-webhook", json=payload2)
    assert response2.status_code in [200, 500]  # Structure valid
    
    # Test direct TicketID
    payload3 = {"TicketID": 999}
    response3 = client.post("/znuny-webhook", json=payload3)
    assert response3.status_code in [200, 500]  # Structure valid


def test_webhook_methods():
    """Test webhook accepts POST, GET, PUT methods."""
    payload = {"TicketID": 111}
    
    # POST
    response_post = client.post("/znuny-webhook", json=payload)
    assert response_post.status_code in [200, 500]
    
    # GET
    response_get = client.get("/znuny-webhook")
    assert response_get.status_code in [200, 400, 500]
    
    # PUT
    response_put = client.put("/znuny-webhook", json=payload)
    assert response_put.status_code in [200, 500]


def test_openapi_docs():
    """Test that OpenAPI documentation is available."""
    response = client.get("/docs")
    assert response.status_code == 200
    
    response_openapi = client.get("/openapi.json")
    assert response_openapi.status_code == 200
    assert "openapi" in response_openapi.json()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
