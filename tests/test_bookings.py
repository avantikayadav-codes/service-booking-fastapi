def test_bookings_require_login(client):
    response = client.get("/bookings/")
    assert response.status_code == 401


def test_booking_with_invalid_service(client, auth_headers):
    response = client.post("/bookings/", json={
        "service_id": 999,
        "booking_date": "2026-12-10T10:00:00",
    }, headers=auth_headers)
    assert response.status_code == 404


def test_view_bookings_empty(client, auth_headers):
    response = client.get("/bookings/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []

def test_create_booking_success(client, auth_headers, service):
    response = client.post("/bookings/", json={
        "service_id": service.id,
        "booking_date": "2026-12-10T10:00:00",
    }, headers=auth_headers)
    assert response.status_code == 200
    assert "id" in response.json()


def test_view_own_booking(client, auth_headers, service):
    created = client.post("/bookings/", json={
        "service_id": service.id,
        "booking_date": "2026-12-10T10:00:00",
    }, headers=auth_headers).json()

    response = client.get(f"/bookings/{created['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_user_can_cancel_booking(client, auth_headers, service):
    created = client.post("/bookings/", json={
        "service_id": service.id,
        "booking_date": "2026-12-10T10:00:00",
    }, headers=auth_headers).json()

    response = client.patch(f"/bookings/{created['id']}",
                            json={"status": "Cancelled"},
                            headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["status"] == "Cancelled"


def test_user_cannot_confirm_booking(client, auth_headers, service):
    created = client.post("/bookings/", json={
        "service_id": service.id,
        "booking_date": "2026-12-10T10:00:00",
    }, headers=auth_headers).json()

    response = client.patch(f"/bookings/{created['id']}",
                            json={"status": "Confirmed"},
                            headers=auth_headers)
    assert response.status_code == 403