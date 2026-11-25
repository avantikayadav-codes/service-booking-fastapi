import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.models.service import Service
from app.models.user import User

from app.main import app
from app.database.database import Base, get_db

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db, monkeypatch):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    # tests mein Redis/Celery nahi chahiye
    monkeypatch.setattr("app.tasks.send_booking_email.delay", lambda *a, **k: None)

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()

@pytest.fixture()
def auth_headers(client):
    client.post("/users/", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "Test@1234",
    })
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "Test@1234",
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture()
def service(db):
    new_service = Service(
        name="AC Repair",
        description="AC cleaning and repair",
        price=999.0,
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

@pytest.fixture()
def admin_headers(client, db):
    client.post("/users/", json={
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "Admin@1234",
    })
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    admin.role = "admin"
    db.commit()

    response = client.post("/auth/login", json={
        "email": "admin@example.com",
        "password": "Admin@1234",
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}