# Service Booking API

A FastAPI backend for booking services, with JWT authentication, role-based access, image uploads and background email tasks.

## Features

- User registration and login (JWT)
- Roles: user, admin, super_admin
- Services CRUD (admin-only create/update/delete) with image upload
- Bookings: users create and cancel their own bookings
- Pagination, filtering and search
- Background booking-confirmation task using Celery + Redis
- Database migrations with Alembic
- Automated tests with pytest
- Docker and Docker Compose setup

## Tech Stack

Python, FastAPI, SQLAlchemy, PostgreSQL, Alembic, Celery, Redis, Pytest, Docker

## Project Structure

```
app/
├── core/        # config, security, dependencies
├── crud/        # database logic
├── database/    # engine and session
├── models/      # SQLAlchemy models
├── routers/     # API endpoints
├── schemas/     # Pydantic schemas
├── celery_app.py
├── tasks.py
└── main.py
alembic/         # migrations
tests/           # pytest tests
```

## Run with Docker

1. Create a `.env` file (see `.env.example`):

```
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

2. Start everything:

```
docker compose up --build
```

3. Open the API docs at `http://127.0.0.1:8000/docs`

Docker Compose starts PostgreSQL, Redis, the API (runs migrations automatically) and the Celery worker.

## Run Tests

```
pip install -r requirements.txt
pytest -v
```

Tests use an in-memory SQLite database and do not need Redis or PostgreSQL.

## API Overview

| Area | Endpoints |
|------|-----------|
| Auth | `POST /auth/login`, `GET /auth/me` |
| Users | `POST /users/`, `GET/PATCH/DELETE /users/{id}` |
| Services | `GET /services/`, `POST /services/` (admin), `POST /services/{id}/upload-image` (admin) |
| Bookings | `POST /bookings/`, `GET /bookings/`, `PATCH /bookings/{id}` |
