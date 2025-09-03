from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "API is online"

def test_analyze_endpoint_success():
    # Use a simple, non-controversial text for testing
    test_text = "Apple announced a new iPhone with improved features."
    response = client.post("/analyze", json={"text": test_text})
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "sentiment" in data
    assert "label" in data["sentiment"]
    assert "score" in data["sentiment"]
    assert len(data["summary"]) > 0

def test_analyze_endpoint_empty_text():
    response = client.post("/analyze", json={"text": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "Text cannot be empty."

def test_analyze_endpoint_invalid_payload():
    response = client.post("/analyze", json={"invalid_key": "some text"})
    assert response.status_code == 422 # Unprocessable Entity