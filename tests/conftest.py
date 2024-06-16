import pytest
import requests
from app import create_app, db, migrate
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    app = create_app(start_db=False)

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "asecret"

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def jwt_token(client):
    username = "testuser"
    password = "t3stP@ssword"
    client.post("/auth/register", json={"username": username, "password": password})

    response = client.post(
        "/auth/login", json={"username": username, "password": password}
    )
    token = response.json["access_token"]
    return token


@pytest.fixture(scope="function")
def create_owner(client, jwt_token):
    owner_name = "Test Owner"
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.post("/main/owners", json={"name": owner_name}, headers=headers)
    assert response.status_code == 201
    owner_id = response.json["id"]
    return owner_id


@pytest.fixture(scope="function")
def create_car(client, jwt_token, create_owner):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.post(
        "/main/cars",
        json={"owner_id": create_owner, "color": "blue", "model": "sedan"},
        headers=headers,
    )
    assert response.status_code == 201
    car_id = response.json["id"]
    return car_id
