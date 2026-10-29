"""
test_categories.py — Category API Tests

Covers:
- GET  /api/v1/categories        (public)
- POST /api/v1/categories        (admin only)
- DELETE /api/v1/categories/{id} (admin only)
"""


class TestGetCategories:
    """Category listing tests"""

    def test_get_categories_empty(self, client):
        """Pehle se koi category nahi — empty list milni chahiye"""
        resp = client.get("/api/v1/categories")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_get_categories_after_create(self, client, admin_user_and_headers):
        """Category create karne ke baad list mein dikhni chahiye"""
        # Create
        client.post("/api/v1/categories", headers=admin_user_and_headers, json={
            "name": "Electronics",
            "description": "Gadgets and devices"
        })
        # Verify
        resp = client.get("/api/v1/categories")
        assert resp.status_code == 200
        categories = resp.json()
        assert len(categories) == 1
        assert categories[0]["name"] == "Electronics"


class TestCreateCategory:
    """Category creation tests"""

    def test_create_category_as_admin(self, client, admin_user_and_headers):
        """Admin new category bana sakta hai"""
        resp = client.post("/api/v1/categories", headers=admin_user_and_headers, json={
            "name": "Clothing",
            "description": "Fashion and apparel"
        })
        assert resp.status_code in (200, 201)
        data = resp.json()
        assert data["name"] == "Clothing"
        assert "id" in data

    def test_create_category_as_customer_forbidden(self, client, auth_headers):
        """Customer category nahi bana sakta — 403 hona chahiye"""
        resp = client.post("/api/v1/categories", headers=auth_headers, json={
            "name": "Hacking",
            "description": "Not allowed"
        })
        assert resp.status_code == 403

    def test_create_category_unauthenticated(self, client):
        """Bina login ke category nahi bana sakta — 401 hona chahiye"""
        resp = client.post("/api/v1/categories", json={
            "name": "Test",
            "description": "Test"
        })
        assert resp.status_code == 401

    def test_create_duplicate_category(self, client, admin_user_and_headers):
        """Same naam ki duplicate category — fail honi chahiye"""
        client.post("/api/v1/categories", headers=admin_user_and_headers, json={
            "name": "Electronics",
            "description": "First"
        })
        resp = client.post("/api/v1/categories", headers=admin_user_and_headers, json={
            "name": "Electronics",
            "description": "Duplicate"
        })
        assert resp.status_code == 400
