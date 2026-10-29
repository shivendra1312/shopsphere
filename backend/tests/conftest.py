"""
conftest.py — Test Configuration
- In-memory SQLite database use karta hai taaki PostgreSQL install karne ki zarurat na ho
- Har test ke baad tables clean ho jaati hain (isolation)
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app as fastapi_app
from app.core.database import Base, get_db
import app.models  # noqa: F401

# In-memory SQLite — no PostgreSQL required for tests
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_db(monkeypatch):
    """Har test se pehle nayi tables bana, test ke baad delete kar do."""
    from app.core import redis as redis_core
    monkeypatch.setattr(redis_core, "get_redis_client", lambda: None)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    """FastAPI ka real DB dependency test DB se replace karna."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    """FastAPI TestClient jo test database use karta hai."""
    fastapi_app.dependency_overrides[get_db] = override_get_db
    with TestClient(fastapi_app) as c:
        yield c
    fastapi_app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def registered_user(client):
    """Helper: Ek test user register aur uski details return karo."""
    resp = client.post("/api/v1/auth/register", json={
        "email": "testuser@example.com",
        "password": "Password123",
        "first_name": "Test",
        "last_name": "User"
    })
    assert resp.status_code == 201
    return {
        "email": "testuser@example.com",
        "password": "Password123",
        "user": resp.json()["user"]
    }


@pytest.fixture(scope="function")
def auth_headers(client, registered_user):
    """Helper: Login karke Bearer token headers return karo."""
    resp = client.post("/api/v1/auth/login", json={
        "email": registered_user["email"],
        "password": registered_user["password"]
    })
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def admin_user_and_headers(client):
    """Helper: Admin user register karo aur uske headers return karo."""
    from sqlalchemy.orm import Session
    from app.models.user import UserRole

    db: Session = TestingSessionLocal()

    # Register
    resp = client.post("/api/v1/auth/register", json={
        "email": "admin@example.com",
        "password": "AdminPass123",
        "first_name": "Admin",
        "last_name": "User"
    })
    assert resp.status_code == 201
    user_id = resp.json()["user"]["id"]

    # DB se role update karo
    from app.models.user import User
    user = db.query(User).filter(User.id == user_id).first()
    user.role = UserRole.ADMIN
    db.commit()
    db.close()

    # Login
    resp = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminPass123"
    })
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
