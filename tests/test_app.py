import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all('description' in v and 'schedule' in v and 'participants' in v for v in data.values())

def test_signup_and_unregister():
    # Use a test email and activity
    test_email = "pytest-student@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))

    # Sign up
    response = client.post(f"/activities/{activity}/signup", json={"email": test_email})
    assert response.status_code == 200
    assert test_email in client.get("/activities").json()[activity]["participants"]

    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert response.status_code == 200
    assert test_email not in client.get("/activities").json()[activity]["participants"]

def test_signup_duplicate():
    test_email = "pytest-dup@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))
    # First signup
    client.post(f"/activities/{activity}/signup", json={"email": test_email})
    # Duplicate signup
    response = client.post(f"/activities/{activity}/signup", json={"email": test_email})
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()
    # Cleanup
    client.post(f"/activities/{activity}/unregister?email={test_email}")
