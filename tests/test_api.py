import os
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    """Test the root status endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI LLM Service is running!"}

def test_generate_llm_stub(monkeypatch):
    """Test the /api/llm/generate endpoint in stub mode."""
    # Force LLM_STUB=1 during this test
    monkeypatch.setenv("LLM_STUB", "1")
    
    payload = {
        "prompt": "What is Python?",
        "system_prompt": "Be concise."
    }
    
    response = client.post("/api/llm/generate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["stubbed"] is True
    assert "[STUB RESPONSE]" in data["content"]
    assert "model" in data

def test_generate_llm_invalid_payload():
    """Test validation error when prompt is missing or empty."""
    payload = {
        "prompt": ""  # Violates min_length=1 schema constraint
    }
    
    response = client.post("/api/llm/generate", json=payload)
    assert response.status_code == 422  # Unprocessable Entity