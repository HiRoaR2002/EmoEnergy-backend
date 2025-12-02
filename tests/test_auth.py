from fastapi.testclient import TestClient
from app.main import app
import random
import string

client = TestClient(app)

def random_email():
    return f"{''.join(random.choices(string.ascii_lowercase, k=10))}@example.com"

def test_signup():
    email = random_email()
    response = client.post(
        "/api/v1/auth/signup",
        json={"email": email, "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert "id" in data

def test_login():
    email = random_email()
    password = "password123"
    
    # Signup first
    client.post(
        "/api/v1/auth/signup",
        json={"email": email, "password": password},
    )
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
