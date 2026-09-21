from fastapi.testclient import TestClient


def register_and_login(
    client: TestClient,
    username: str = "noteuser",
    email: str = "noteuser@example.com",
) -> dict[str, str]:
    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "matkhau123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "matkhau123",
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {access_token}",
    }


def create_note(
    client: TestClient,
    headers: dict[str, str],
    title: str = "Note test",
    content: str = "Nội dung test",
) -> dict:
    response = client.post(
        "/notes/",
        headers=headers,
        json={
            "title": title,
            "content": content,
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_note_success(
    client: TestClient,
) -> None:
    headers = register_and_login(client)

    response = client.post(
        "/notes/",
        headers=headers,
        json={
            "title": "Note đầu tiên",
            "content": "Nội dung đầu tiên",
        },
    )

    assert response.status_code == 201

    note = response.json()

    assert note["title"] == "Note đầu tiên"
    assert note["content"] == "Nội dung đầu tiên"

    current_user = client.get(
        "/auth/me",
        headers=headers,
    ).json()

    assert note["owner_id"] == current_user["id"]


def test_get_my_notes(
    client: TestClient,
) -> None:
    headers = register_and_login(client)

    create_note(
        client,
        headers,
        title="Note 1",
    )

    create_note(
        client,
        headers,
        title="Note 2",
    )

    response = client.get(
        "/notes/",
        headers=headers,
    )

    assert response.status_code == 200

    notes = response.json()

    assert len(notes) == 2
    assert notes[0]["title"] == "Note 1"
    assert notes[1]["title"] == "Note 2"


def test_update_my_note(
    client: TestClient,
) -> None:
    headers = register_and_login(client)
    note = create_note(client, headers)

    response = client.put(
        f"/notes/{note['id']}",
        headers=headers,
        json={
            "title": "Tiêu đề đã sửa",
            "content": "Nội dung đã sửa",
        },
    )

    assert response.status_code == 200

    updated_note = response.json()

    assert updated_note["title"] == "Tiêu đề đã sửa"
    assert updated_note["content"] == "Nội dung đã sửa"


def test_delete_my_note(
    client: TestClient,
) -> None:
    headers = register_and_login(client)
    note = create_note(client, headers)

    delete_response = client.delete(
        f"/notes/{note['id']}",
        headers=headers,
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/notes/{note['id']}",
        headers=headers,
    )

    assert get_response.status_code == 404


def test_user_cannot_access_another_users_note(
    client: TestClient,
) -> None:
    user_one_headers = register_and_login(
        client,
        username="userone",
        email="userone@example.com",
    )

    note = create_note(
        client,
        user_one_headers,
        title="Note của user one",
    )

    user_two_headers = register_and_login(
        client,
        username="usertwo",
        email="usertwo@example.com",
    )

    get_response = client.get(
        f"/notes/{note['id']}",
        headers=user_two_headers,
    )

    update_response = client.put(
        f"/notes/{note['id']}",
        headers=user_two_headers,
        json={
            "title": "Chiếm quyền sửa",
            "content": "Không được phép",
        },
    )

    delete_response = client.delete(
        f"/notes/{note['id']}",
        headers=user_two_headers,
    )

    assert get_response.status_code == 404
    assert update_response.status_code == 404
    assert delete_response.status_code == 404

    owner_response = client.get(
        f"/notes/{note['id']}",
        headers=user_one_headers,
    )

    assert owner_response.status_code == 200
def test_create_note_with_day51_fields(
    client: TestClient,
) -> None:

    headers = register_and_login(client)

    response = client.post(
        "/notes/",
        headers=headers,
        json={
            "title": "Học Day 51",
            "content": "Test field mới",
            "completed": False,
            "due_date": "2026-09-25T20:00:00",
            "tags": [
                "python",
                "fastapi",
            ],
        },
    )

    assert response.status_code == 201

    note = response.json()

    assert note["completed"] is False

    assert note["tags"] == [
        "python",
        "fastapi",
    ]

    assert note["due_date"] is not None
def test_mark_note_completed(
    client: TestClient,
) -> None:

    headers = register_and_login(client)

    note = create_note(
        client,
        headers,
    )

    response = client.put(
        f"/notes/{note['id']}",
        headers=headers,
        json={
            "completed": True,
        },
    )

    assert response.status_code == 200

    assert (
        response.json()["completed"]
        is True
    )
def test_remove_note_due_date(
    client: TestClient,
) -> None:
    headers = register_and_login(client)

    response = client.post(
        "/notes/",
        headers=headers,
        json={
            "title": "Note có deadline",
            "content": "Test due date",
            "due_date": "2026-09-25T20:00:00",
        },
    )

    assert response.status_code == 201

    note = response.json()

    update_response = client.put(
        f"/notes/{note['id']}",
        headers=headers,
        json={
            "due_date": None,
        },
    )

    assert update_response.status_code == 200

    updated_note = update_response.json()

    assert updated_note["due_date"] is None
def test_normalize_note_tags(
    client: TestClient,
) -> None:
    headers = register_and_login(client)

    response = client.post(
        "/notes/",
        headers=headers,
        json={
            "title": "Test tags",
            "content": "Kiểm tra normalize tags",
            "tags": [
                " Python ",
                "FASTAPI",
                "python",
                " API ",
            ],
        },
    )

    assert response.status_code == 201

    assert response.json()["tags"] == [
        "python",
        "fastapi",
        "api",
    ]