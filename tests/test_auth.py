def test_register_user(client):
    response = client.post("/users/", json={
        "name": "Avantika",
        "email": "avantika@example.com",
        "password": "Test@1234",
    })
    assert response.status_code == 200
    assert response.json()["email"] == "avantika@example.com"


def test_login_success(client):
    client.post("/users/", json={
        "name": "Avantika",
        "email": "avantika@example.com",
        "password": "Test@1234",
    })
    response = client.post("/auth/login", json={
        "email": "avantika@example.com",
        "password": "Test@1234",
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post("/users/", json={
        "name": "Avantika",
        "email": "avantika@example.com",
        "password": "Test@1234",
    })
    response = client.post("/auth/login", json={
        "email": "avantika@example.com",
        "password": "wrong-password",
    })
    assert response.status_code == 401


def test_me_with_token(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"