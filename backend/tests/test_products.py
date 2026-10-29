"""
test_products.py — Product API Tests

Covers:
- GET  /api/v1/products          (public, search, filter)
- GET  /api/v1/products/{id}     (public)
- POST /api/v1/products          (admin only)
- PUT  /api/v1/products/{id}     (admin only)
- DELETE /api/v1/products/{id}   (admin only)
"""


def create_test_category(client, admin_headers):
    """Helper: test ke liye ek category banao"""
    resp = client.post("/api/v1/categories", headers=admin_headers, json={
        "name": "Test Category",
        "description": "For testing"
    })
    assert resp.status_code in (200, 201)
    return resp.json()["id"]


def create_test_product(client, admin_headers, category_id, title="Test Product", price=99.99, stock=10):
    """Helper: test ke liye ek product banao"""
    resp = client.post("/api/v1/products", headers=admin_headers, json={
        "title": title,
        "description": "A test product description",
        "price": price,
        "stock": stock,
        "category_id": category_id
    })
    assert resp.status_code in (200, 201)
    return resp.json()


class TestGetProducts:
    """Product listing tests"""

    def test_get_products_empty(self, client):
        """Pehle koi product nahi — empty list milni chahiye"""
        resp = client.get("/api/v1/products")
        assert resp.status_code == 200
        data = resp.json()
        # Paginatd ya list — dono handle karo
        items = data.get("items", data) if isinstance(data, dict) else data
        assert isinstance(items, list)

    def test_get_products_returns_list(self, client, admin_user_and_headers):
        """Product create karne ke baad list mein dikhna chahiye"""
        cat_id = create_test_category(client, admin_user_and_headers)
        create_test_product(client, admin_user_and_headers, cat_id)

        resp = client.get("/api/v1/products")
        assert resp.status_code == 200
        data = resp.json()
        items = data.get("items", data) if isinstance(data, dict) else data
        assert len(items) >= 1

    def test_search_products(self, client, admin_user_and_headers):
        """Product search by title"""
        cat_id = create_test_category(client, admin_user_and_headers)
        create_test_product(client, admin_user_and_headers, cat_id, title="iPhone 15 Pro")
        create_test_product(client, admin_user_and_headers, cat_id, title="Samsung Galaxy S24")

        resp = client.get("/api/v1/products?search=iPhone")
        assert resp.status_code == 200
        data = resp.json()
        items = data.get("items", data) if isinstance(data, dict) else data
        assert any("iPhone" in p["title"] for p in items)


class TestGetProduct:
    """Single product tests"""

    def test_get_existing_product(self, client, admin_user_and_headers):
        """Existing product ID se detail milni chahiye"""
        cat_id = create_test_category(client, admin_user_and_headers)
        product = create_test_product(client, admin_user_and_headers, cat_id)

        resp = client.get(f"/api/v1/products/{product['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == product["id"]
        assert resp.json()["title"] == product["title"]

    def test_get_nonexistent_product(self, client):
        """Galat ID se product — 404 hona chahiye"""
        resp = client.get("/api/v1/products/99999")
        assert resp.status_code == 404


class TestCreateProduct:
    """Product creation tests"""

    def test_create_product_as_admin(self, client, admin_user_and_headers):
        """Admin product bana sakta hai"""
        cat_id = create_test_category(client, admin_user_and_headers)
        resp = client.post("/api/v1/products", headers=admin_user_and_headers, json={
            "title": "New Laptop",
            "description": "High performance laptop",
            "price": 999.99,
            "stock": 50,
            "category_id": cat_id
        })
        assert resp.status_code in (200, 201)
        data = resp.json()
        assert data["title"] == "New Laptop"
        assert data["price"] == 999.99
        assert "id" in data

    def test_create_product_as_customer_forbidden(self, client, auth_headers, admin_user_and_headers):
        """Customer product nahi bana sakta — 403"""
        cat_id = create_test_category(client, admin_user_and_headers)
        resp = client.post("/api/v1/products", headers=auth_headers, json={
            "title": "Fake Product",
            "description": "Not allowed",
            "price": 1.0,
            "stock": 1,
            "category_id": cat_id
        })
        assert resp.status_code == 403

    def test_create_product_invalid_price(self, client, admin_user_and_headers):
        """Negative price — fail hona chahiye"""
        cat_id = create_test_category(client, admin_user_and_headers)
        resp = client.post("/api/v1/products", headers=admin_user_and_headers, json={
            "title": "Bad Product",
            "description": "Invalid price",
            "price": -10.0,
            "stock": 5,
            "category_id": cat_id
        })
        # Either 422 (validation) or 400 (business logic)
        assert resp.status_code in (400, 422)

    def test_create_product_nonexistent_category(self, client, admin_user_and_headers):
        """Galat category_id se product — fail hona chahiye"""
        resp = client.post("/api/v1/products", headers=admin_user_and_headers, json={
            "title": "Orphan Product",
            "description": "No category",
            "price": 50.0,
            "stock": 5,
            "category_id": 99999
        })
        assert resp.status_code in (400, 404, 422)


class TestDeleteProduct:
    """Product deletion tests"""

    def test_delete_product_as_admin(self, client, admin_user_and_headers):
        """Admin product delete kar sakta hai"""
        cat_id = create_test_category(client, admin_user_and_headers)
        product = create_test_product(client, admin_user_and_headers, cat_id)

        resp = client.delete(f"/api/v1/products/{product['id']}", headers=admin_user_and_headers)
        assert resp.status_code in (200, 204)

        # Verify deleted
        resp2 = client.get(f"/api/v1/products/{product['id']}")
        assert resp2.status_code == 404

    def test_delete_product_as_customer_forbidden(self, client, auth_headers, admin_user_and_headers):
        """Customer product delete nahi kar sakta — 403"""
        cat_id = create_test_category(client, admin_user_and_headers)
        product = create_test_product(client, admin_user_and_headers, cat_id)

        resp = client.delete(f"/api/v1/products/{product['id']}", headers=auth_headers)
        assert resp.status_code == 403
