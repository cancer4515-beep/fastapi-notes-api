from fastapi.testclient import TestClient


def test_get_notes_without_token(
    client: TestClient,
) -> None:
    response = client.get("/notes/")

    assert response.status_code == 401


def test_create_note_without_token(
    client: TestClient,
) -> None:
    response = client.post(
        "/notes/",
        json={
            "title": "Note không hợp lệ",
            "content": "Không có JWT",
        },
    )

    assert response.status_code == 401


def test_update_note_without_token(
    client: TestClient,
) -> None:
    response = client.put(
        "/notes/1",
        json={
            "title": "Tiêu đề mới",
            "content": "Nội dung mới",
        },
    )

    assert response.status_code == 401


def test_delete_note_without_token(
    client: TestClient,
) -> None:
    response = client.delete("/notes/1")

    assert response.status_code == 401