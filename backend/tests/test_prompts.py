import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_prompt():
    payload = {"text": "Test prompt for optimization"}
    response = client.post("/api/v1/prompts/generate-prompt", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["received_text"] == "Test prompt for optimization"
    assert data["status"] == "ok"

def test_generate_prompt_invalid_payload():
    # Test with missing 'text' field
    payload = {"not_text": "Invalid"}
    response = client.post("/api/v1/prompts/generate-prompt", json=payload)
    
    assert response.status_code == 422  # Validation Error
