from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_generate_algebra_easy_is_deterministic() -> None:
    payload = {"subject": "algebra", "tier": "easy"}

    first = client.post("/generate", json=payload)
    second = client.post("/generate", json=payload)

    assert first.status_code == 200
    assert first.json() == second.json()
    assert first.json() == {
        "subject": "algebra",
        "tier": "easy",
        "problem": "Solve for x: 2*x + 3 = 11",
        "solution": "x = 4",
    }


def test_generate_arithmetic_exam() -> None:
    response = client.post(
        "/generate",
        json={"subject": "arithmetic", "tier": "exam"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "subject": "arithmetic",
        "tier": "exam",
        "problem": "Compute: (7/8) * (2/3) + 5/12",
        "solution": "1",
    }


def test_generate_rejects_unsupported_subject() -> None:
    response = client.post(
        "/generate",
        json={"subject": "geometry", "tier": "easy"},
    )

    assert response.status_code == 400
    body = response.json()
    assert "Unsupported subject 'geometry'" in body["detail"]["message"]
    assert body["detail"]["supported_subjects"] == ["algebra", "arithmetic"]


def test_generate_rejects_unsupported_tier() -> None:
    response = client.post(
        "/generate",
        json={"subject": "algebra", "tier": "beginner"},
    )

    assert response.status_code == 422


def test_health_lists_supported_subjects() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "supported_subjects": ["algebra", "arithmetic"],
    }
