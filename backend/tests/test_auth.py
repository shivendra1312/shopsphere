"""
test_auth.py — Authentication API Tests

Covers:
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET  /api/v1/auth/me
"""


class TestRegister:
    """User Registration Tests"""

    def test_register_success(self, client):
        """Naye user ka successful registration"""
        resp = client.post("/api/v1/auth/register", json={
            "email": "newuser@example.com",
            "password": "Password123",
            "first_name": "New",
            "last_name": "User"
        })
        assert resp.status_code == 201
        data = resp.json()
        assert "user" in data
        assert data["user"]["email"] == "newuser@example.com"
        assert data["user"]["first_name"] == "New"
        assert data["user"]["role"] == "CUSTOMER"
        assert "password" not in data["user"]  # Password kabhi expose nahi hona chahiye

    def test_register_duplicate_email(self, client, registered_user):
        """Same email se dobara register karne ki koshish — fail honi chahiye"""
        resp = client.post("/api/v1/auth/register", json={
            "email": registered_user["email"],  # already registered
            "password": "AnotherPass123",
            "first_name": "Duplicate",
            "last_name": "User"
        })
        assert resp.status_code == 400

    def test_register_invalid_email(self, client):
        """Invalid email format se register — fail hona chahiye"""
        resp = client.post("/api/v1/auth/register", json={
            "email": "not-an-email",
            "password": "Password123",
            "first_name": "Test",
            "last_name": "User"
        })
        assert resp.status_code == 422  # Validation error

    def test_register_short_password(self, client):
        """8 characters se chhota password — fail hona chahiye"""
        resp = client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "password": "short",
            "first_name": "Test",
            "last_name": "User"
        })
        assert resp.status_code == 422

    def test_register_missing_fields(self, client):
        """Required fields missing — fail hona chahiye"""
        resp = client.post("/api/v1/auth/register", json={
            "email": "test@example.com"
            # password, first_name, last_name missing
        })
        assert resp.status_code == 422


class TestLogin:
    """User Login Tests"""

    def test_login_success(self, client, registered_user):
        """Valid credentials se login — access + refresh tokens milne chahiye"""
        resp = client.post("/api/v1/auth/login", json={
            "email": registered_user["email"],
            "password": registered_user["password"]
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, registered_user):
        """Galat password se login — fail hona chahiye"""
        resp = client.post("/api/v1/auth/login", json={
            "email": registered_user["email"],
            "password": "WrongPassword123"
        })
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client):
        """Unregistered email se login — fail hona chahiye"""
        resp = client.post("/api/v1/auth/login", json={
            "email": "nobody@example.com",
            "password": "Password123"
        })
        assert resp.status_code == 401


class TestMe:
    """Current User Profile Tests"""

    def test_me_authenticated(self, client, registered_user, auth_headers):
        """Valid token se /me — user data milna chahiye"""
        resp = client.get("/api/v1/auth/me", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == registered_user["email"]

    def test_me_no_token(self, client):
        """/me bina token ke — 401 hona chahiye"""
        resp = client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    def test_me_invalid_token(self, client):
        """/me fake token se — 401 hona chahiye"""
        resp = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer fakejwt123"})
        assert resp.status_code == 401
