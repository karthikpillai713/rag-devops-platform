
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_search_endpoint():
    fake_result = {
        "question": "What is Docker used for?",
        "answer": "Docker packages applications into containers.",
        "sources": ["devops-basics.txt"],
    }

    with patch(
        "app.main.answer_question",
        return_value=fake_result,
    ) as mock_answer:
        response = client.post(
            "/search",
            json={
                "question": "What is Docker used for?",
                "top_k": 2,
            },
        )

    assert response.status_code == 200
    assert response.json() == fake_result

    mock_answer.assert_called_once_with(
        question="What is Docker used for?",
        top_k=2,
    )
