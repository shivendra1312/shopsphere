"""
test_cart.py — Shopping Cart API Tests

Covers:
- GET    /api/v1/cart                  (user's cart)
- POST   /api/v1/cart                  (add item)
- PUT    /api/v1/cart/{item_id}        (update quantity)
- DELETE /api/v1/cart/{item_id}        (remove item)
"""


def create_test_product_in_db(client, admin_headers):
    """Helper: Category + Product bana kar product return karo"""
    cat_resp = client.post("/api/v1/categories", headers=admin_headers, json={
        "name": "CartTest Category",
        "description": "Testing"
    })
    cat_id = cat_resp.json()["id"]

    prod_resp = client.post("/api/v1/products", headers=admin_headers, json={
        "title": "CartTest Product",
        "description": "A product for cart testing",
        "price": 49.99,
        "stock": 100,
        "category_id": cat_id
    })
    return prod_resp.json()


class TestGetCart:
    """Cart listing tests"""

    def test_get_empty_cart(self, client, auth_headers):
        """Naye user ka cart pehle se khali honi chahiye"""
        resp = client.get("/api/v1/cart", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json() == []

    def test_get_cart_unauthenticated(self, client):
        """Bina login ke cart nahi dekh sakte — 401"""
        resp = client.get("/api/v1/cart")
        assert resp.status_code == 401


class TestAddToCart:
    """Add to cart tests"""

    def test_add_item_to_cart(self, client, auth_headers, admin_user_and_headers):
        """Product cart mein add hona chahiye"""
        product = create_test_product_in_db(client, admin_user_and_headers)

        resp = client.post("/api/v1/cart", headers=auth_headers, json={
            "product_id": product["id"],
            "quantity": 2
        })
        assert resp.status_code in (200, 201)
        data = resp.json()
        assert data["product_id"] == product["id"]
        assert data["quantity"] == 2

    def test_add_same_item_twice_updates_quantity(self, client, auth_headers, admin_user_and_headers):
        """Same product dobara add karne se quantity update honi chahiye"""
        product = create_test_product_in_db(client, admin_user_and_headers)

        client.post("/api/v1/cart", headers=auth_headers, json={
            "product_id": product["id"],
            "quantity": 1
        })
        client.post("/api/v1/cart", headers=auth_headers, json={
            "product_id": product["id"],
            "quantity": 2
        })

        resp = client.get("/api/v1/cart", headers=auth_headers)
        cart = resp.json()
        assert len(cart) == 1  # Ek hi item honi chahiye
        assert cart[0]["quantity"] == 3  # 1 + 2 = 3

    def test_add_nonexistent_product(self, client, auth_headers):
        """Galat product cart mein add nahi ho sakta — 404"""
        resp = client.post("/api/v1/cart", headers=auth_headers, json={
            "product_id": 99999,
            "quantity": 1
        })
        assert resp.status_code == 404


class TestRemoveFromCart:
    """Remove from cart tests"""

    def test_remove_item_from_cart(self, client, auth_headers, admin_user_and_headers):
        """Cart item delete karna"""
        product = create_test_product_in_db(client, admin_user_and_headers)

        # Add
        add_resp = client.post("/api/v1/cart", headers=auth_headers, json={
            "product_id": product["id"],
            "quantity": 1
        })
        item_id = add_resp.json()["id"]

        # Delete
        del_resp = client.delete(f"/api/v1/cart/{item_id}", headers=auth_headers)
        assert del_resp.status_code in (200, 204)

        # Verify empty
        cart_resp = client.get("/api/v1/cart", headers=auth_headers)
        assert cart_resp.json() == []

    def test_remove_others_cart_item_forbidden(self, client, auth_headers, admin_user_and_headers):
        """Kisi aur ke cart item ko delete nahi kar sakte"""
        product = create_test_product_in_db(client, admin_user_and_headers)

        # Admin ka cart item banao
        add_resp = client.post("/api/v1/cart", headers=admin_user_and_headers, json={
            "product_id": product["id"],
            "quantity": 1
        })
        admin_item_id = add_resp.json()["id"]

        # Regular user se delete karne ki koshish (fails or ignores gracefully)
        client.delete(f"/api/v1/cart/{admin_item_id}", headers=auth_headers)

        # Admin ka cart item abhi bhi intact hona chahiye
        admin_cart = client.get("/api/v1/cart", headers=admin_user_and_headers).json()
        assert len(admin_cart) == 1
        assert admin_cart[0]["id"] == admin_item_id
