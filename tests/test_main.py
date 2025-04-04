import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app, get_db
from src.database import Base

# Create a new database for testing
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/test_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the test database
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_register_user():
    response = client.post(
        "/api/users/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_user():
    # First, register the user
    client.post(
        "/api/users/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    # Then, login with the same credentials
    response = client.post(
        "/api/users/login",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_logout_user():
    # First, register and login the user
    register_response = client.post(
        "/api/users/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    access_token = register_response.json()["access_token"]
    # Then, logout the user
    response = client.post(
        "/api/users/logout",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Logged out successfully"}

def test_refresh_token():
    # First, register and login the user
    register_response = client.post(
        "/api/users/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    access_token = register_response.json()["access_token"]
    # Then, refresh the token
    response = client.post(
        "/api/auth/refresh",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_read_users_me():
    # First, register and login the user
    register_response = client.post(
        "/api/users/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    access_token = register_response.json()["access_token"]
    # Then, get the current user data
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"