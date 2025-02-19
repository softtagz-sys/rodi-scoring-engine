from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_scoring_valid():
    """Test een correcte scoring-aanvraag."""
    response = client.post("/scoring/", json={
        "model_answer": "Inflatie is het stijgen van prijzen.",
        "student_answer": "Prijzen stijgen door inflatie.",
        "keywords": ["inflatie", "prijzen"]
    })
    assert response.status_code == 200
    json_response = response.json()
    assert "score" in json_response
    assert isinstance(json_response["score"], float)  # Verwacht een numerieke score

def test_scoring_missing_field():
    """Test als een verplichte field ontbreekt."""
    response = client.post("/scoring/", json={
        "student_answer": "Prijzen stijgen door inflatie.",
        "keywords": ["inflatie", "prijzen"]
    })
    assert response.status_code == 422  # Unprocessable Entity (validatiefout FastAPI)

def test_scoring_empty_strings():
    """Test als lege strings worden ingevoerd."""
    response = client.post("/scoring/", json={
        "model_answer": "",
        "student_answer": "",
        "keywords": []
    })
    assert response.status_code == 400  # Bad Request
    assert "detail" in response.json()

def test_scoring_no_keywords():
    """Test wat er gebeurt als er geen keywords worden meegegeven."""
    response = client.post("/scoring/", json={
        "model_answer": "Inflatie is het stijgen van prijzen.",
        "student_answer": "Prijzen stijgen door inflatie.",
        "keywords": []
    })
    assert response.status_code == 200
    json_response = response.json()
    assert "score" in json_response
    assert isinstance(json_response["score"], float)
