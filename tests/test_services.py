import io
from PIL import Image



def test_list_services_public(client, service):
    response = client.get("/services/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_service_not_found(client):
    response = client.get("/services/999")
    assert response.status_code == 404


def test_user_cannot_create_service(client, auth_headers):
    response = client.post("/services/", json={
        "name": "Plumbing",
        "description": "Pipe repair",
        "price": 500.0,
    }, headers=auth_headers)
    assert response.status_code == 403


def test_admin_can_create_service(client, admin_headers):
    response = client.post("/services/", json={
        "name": "Plumbing",
        "description": "Pipe repair",
        "price": 500.0,
    }, headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Plumbing"


def test_upload_requires_admin(client, auth_headers, service):
    response = client.post(
        f"/services/{service.id}/upload-image",
        files={"image": ("fake.png", b"not an image", "image/png")},
        headers=auth_headers,
    )
    assert response.status_code == 403


def test_upload_rejects_fake_image(client, admin_headers, service):
    response = client.post(
        f"/services/{service.id}/upload-image",
        files={"image": ("fake.png", b"not an image", "image/png")},
        headers=admin_headers,
    )
    assert response.status_code == 400


def make_png_bytes():
    buffer = io.BytesIO()
    Image.new("RGB", (10, 10), "red").save(buffer, format="PNG")
    return buffer.getvalue()


def test_admin_can_upload_valid_image(client, admin_headers, service, tmp_path, monkeypatch):
    monkeypatch.setattr("app.routers.services.UPLOAD_DIR", tmp_path)

    response = client.post(
        f"/services/{service.id}/upload-image",
        files={"image": ("photo.png", make_png_bytes(), "image/png")},
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json()["image_path"].endswith(".png")
    assert len(list(tmp_path.iterdir())) == 1


def test_upload_rejects_large_file(client, admin_headers, service, tmp_path, monkeypatch):
    monkeypatch.setattr("app.routers.services.UPLOAD_DIR", tmp_path)

    big_file = b"0" * (5 * 1024 * 1024 + 1)
    response = client.post(
        f"/services/{service.id}/upload-image",
        files={"image": ("big.png", big_file, "image/png")},
        headers=admin_headers,
    )
    assert response.status_code == 413