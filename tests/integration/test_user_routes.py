from app.models import User
from app.security import verify_password


def test_register_user(client):
    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data
    assert "password_hash" not in data


def test_register_user_saves_hashed_password(
    client,
):
    response = client.post(
        "/users/register",
        json={
            "username": "secureuser",
            "email": "secure@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 201

    from tests.conftest import TestingSessionLocal

    db = TestingSessionLocal()

    try:
        user = (
            db.query(User)
            .filter(
                User.email == "secure@example.com"
            )
            .first()
        )

        assert user is not None
        assert user.password_hash != "Password123"
        assert verify_password(
            "Password123",
            user.password_hash,
        )
    finally:
        db.close()


def test_register_duplicate_email(client):
    user_data = {
        "username": "firstuser",
        "email": "duplicate@example.com",
        "password": "Password123",
    }

    first_response = client.post(
        "/users/register",
        json=user_data,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/users/register",
        json={
            "username": "seconduser",
            "email": "duplicate@example.com",
            "password": "Password123",
        },
    )

    assert second_response.status_code == 409
    assert (
        second_response.json()["error"]
        == "Email is already registered"
    )


def test_register_duplicate_username(client):
    first_response = client.post(
        "/users/register",
        json={
            "username": "duplicateuser",
            "email": "first@example.com",
            "password": "Password123",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/users/register",
        json={
            "username": "duplicateuser",
            "email": "second@example.com",
            "password": "Password123",
        },
    )

    assert second_response.status_code == 409
    assert (
        second_response.json()["error"]
        == "Username is already registered"
    )


def test_login_user(client):
    register_response = client.post(
        "/users/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "Password123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/users/login",
        json={
            "email": "login@example.com",
            "password": "Password123",
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert data["username"] == "loginuser"
    assert data["email"] == "login@example.com"


def test_login_with_wrong_password(client):
    register_response = client.post(
        "/users/register",
        json={
            "username": "wrongpassword",
            "email": "wrong@example.com",
            "password": "Password123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/users/login",
        json={
            "email": "wrong@example.com",
            "password": "WrongPassword123",
        },
    )

    assert login_response.status_code == 401
    assert (
        login_response.json()["error"]
        == "Invalid email or password"
    )


def test_login_nonexistent_user(client):
    response = client.post(
        "/users/login",
        json={
            "email": "missing@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 401
    assert (
        response.json()["error"]
        == "Invalid email or password"
    )


def test_register_invalid_email(client):
    response = client.post(
        "/users/register",
        json={
            "username": "bademail",
            "email": "not-an-email",
            "password": "Password123",
        },
    )

    assert response.status_code == 400
    assert "email" in response.json()["error"]