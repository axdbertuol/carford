from werkzeug.security import generate_password_hash

from app.models import User
from app import db


def test_register(client):
    # Test successful registration
    password = "pasSword123@"

    data = {"username": "testuser", "password": password}
    response = client.post("/auth/register", json=data)
    assert response.status_code == 201
    assert response.json["msg"] == "User registered!"

    # Test registration with existing username
    response = client.post("/auth/register", json=data)
    assert response.status_code == 409
    assert response.json["msg"] == "User already exists"


def test_login(client):
    # Create a user for login testing
    password = "pasSword123@"
    hashed_password = generate_password_hash(password)
    user = User(username="testuser", password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()

    # Test successful login
    data = {"username": "testuser", "password": password}
    response = client.post("/auth/login", json=data)
    assert response.status_code == 200
    assert "access_token" in response.json

    # Test login with wrong credentials
    data = {"username": "testuser", "password": "wr0ngp4Ssw@rd"}
    response = client.post("/auth/login", json=data)
    assert response.status_code == 409
    assert response.json["msg"] == "Wrong credentials"
