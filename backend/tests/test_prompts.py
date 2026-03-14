import pytest
from fastapi.testclient import TestClient
from app.main import app

from unittest.mock import AsyncMock
from app.services.prompt_service import get_prompt_service

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_prompt_service():
    mock_service = AsyncMock()
    mock_service.generate_optimized_prompt.return_value = "Optimized: Test prompt for optimization"
    app.dependency_overrides[get_prompt_service] = lambda: mock_service
    yield mock_service
    app.dependency_overrides.clear()

def test_generate_prompt(mock_prompt_service):
    payload = {"text": "Test prompt for optimization"}
    response = client.post("/api/v1/prompts/generate-prompt", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["received_text"] == "Test prompt for optimization"
    assert data["optimized_text"] == "Optimized: Test prompt for optimization"
    assert data["status"] == "ok"

def test_generate_prompt_invalid_payload():
    # Test with missing 'text' field
    payload = {"not_text": "Invalid"}
    response = client.post("/api/v1/prompts/generate-prompt", json=payload)
    
    assert response.status_code == 422  # Validation Error
