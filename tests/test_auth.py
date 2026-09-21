from fastapi.testclient import TestClient


USER_DATA = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "matkhau123",
}


def register_user(client: TestClient):
    return client.post(
        "/auth/register",
        json=USER_DATA,
    )


def test_register_success(client: TestClient) -> None:
    response = register_user(client)

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    assert data["is_active"] is True

    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_username(
    client: TestClient,
) -> None:
    first_response = register_user(client)

    second_response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "another@example.com",
            "password": "matkhau123",
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_login_success(client: TestClient) -> None:
    register_user(client)

    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "matkhau123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


def test_login_wrong_password(
    client: TestClient,
) -> None:
    register_user(client)

    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "matkhau_sai",
        },
    )

    assert response.status_code == 401