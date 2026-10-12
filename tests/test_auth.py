from tests.conftest import auth_header, register_user


def test_register_login_and_me(client):
    token, user = register_user(
        client,
        email="new@example.com",
        display_name="New Voter",
    )
    me = client.get("/auth/me", headers=auth_header(token))
    assert me.status_code == 200
    assert me.json()["email"] == "new@example.com"
    assert me.json()["display_name"] == "New Voter"
    assert me.json()["role"] == "user"

    login = client.post(
        "/auth/login",
        json={"email": "new@example.com", "password": "password123"},
    )
    assert login.status_code == 200
    assert login.json()["user"]["id"] == user["id"]


def test_duplicate_registration_is_rejected(client):
    register_user(client, email="dup@example.com", display_name="Dup One")
    again = client.post(
        "/auth/register",
        json={
            "email": "dup@example.com",
            "display_name": "Dup Two",
            "password": "password123",
        },
    )
    assert again.status_code == 409


def test_wrong_password_is_rejected(client):
    register_user(client, email="bad@example.com", display_name="Bad Login")
    login = client.post(
        "/auth/login",
        json={"email": "bad@example.com", "password": "wrong-password"},
    )
    assert login.status_code == 401
