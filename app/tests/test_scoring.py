from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_scoring():
    response = client.post("/scoring/", json={
        "model_answer": "Inflatie is het stijgen van prijzen.",
        "student_answer": "Prijzen stijgen door inflatie.",
        "keywords": ["inflatie", "prijzen"]
    })
    assert response.status_code == 200
    assert "score" in response.json()
