def test_create_product(client, auth_headers):
    """Test creating a product"""
    product_data = {
        "name": "New Product",
        "price": 49.99,
        "stock": 50,
        "low_stock_threshold": 5,
    }
    response = client.post("/products", json=product_data, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["price"] == product_data["price"]
    assert data["stock"] == product_data["stock"]
    assert data["low_stock_threshold"] == product_data["low_stock_threshold"]
    assert "id" in data


def test_create_product_without_auth(client):
    """Test that creating a product requires authentication"""
    product_data = {
        "name": "New Product",
        "price": 49.99,
        "stock": 50,
        "low_stock_threshold": 5,
    }
    response = client.post("/products", json=product_data)

    assert response.status_code == 401


def test_get_all_products(client, test_product):
    """Test getting all products"""
    response = client.get("/products")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["id"] == test_product["id"]


def test_get_product_by_id(client, test_product):
    """Test getting a specific product"""
    response = client.get(f"/products/{test_product['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_product["id"]
    assert data["name"] == test_product["name"]


def test_get_nonexistent_product(client):
    """Test getting a product that doesn't exist"""
    response = client.get("/products/99999")

    assert response.status_code == 404


def test_update_product(client, auth_headers, test_product):
    """Test updating a product"""
    update_data = {"name": "Updated Product", "price": 39.99}
    response = client.patch(
        f"/products/{test_product['id']}", json=update_data, headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["price"] == update_data["price"]
    assert data["stock"] == test_product["stock"]


def test_delete_product(client, auth_headers, test_product):
    """Test deleting a product"""
    response = client.delete(f"/products/{test_product['id']}", headers=auth_headers)

    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/products/{test_product['id']}")
    assert get_response.status_code == 404


def test_search_products(client, auth_headers):
    """Test searching products"""
    # Create multiple products
    products = [
        {"name": "Red Shirt", "price": 20.00, "stock": 10, "low_stock_threshold": 5},
        {"name": "Blue Shirt", "price": 25.00, "stock": 15, "low_stock_threshold": 5},
        {"name": "Red Pants", "price": 40.00, "stock": 8, "low_stock_threshold": 5},
    ]
    for product in products:
        client.post("/products", json=product, headers=auth_headers)

    # Search for "Shirt"
    response = client.get("/products/search?search=Shirt")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all("Shirt" in p["name"] for p in data)


def test_low_stock_products(client, auth_headers):
    """Test getting low stock products"""
    # Create products with different stock levels
    products = [
        {"name": "High Stock", "price": 20.00, "stock": 50, "low_stock_threshold": 10},
        {"name": "Low Stock", "price": 25.00, "stock": 5, "low_stock_threshold": 10},
        {"name": "Out of Stock", "price": 30.00, "stock": 0, "low_stock_threshold": 10},
    ]
    for product in products:
        client.post("/products", json=product, headers=auth_headers)

    response = client.get("/products/low-stock")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Low Stock and Out of Stock
    assert all(p["stock"] <= p["low_stock_threshold"] for p in data)


def test_pagination(client, auth_headers):
    """Test product pagination"""
    # Create 5 products
    for i in range(5):
        product_data = {
            "name": f"Product {i}",
            "price": 10.00 + i,
            "stock": 10,
            "low_stock_threshold": 5,
        }
        client.post("/products", json=product_data, headers=auth_headers)

    # Get first 2 products
    response = client.get("/products?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # Get next 2 products
    response = client.get("/products?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
