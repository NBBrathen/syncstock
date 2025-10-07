def test_create_order(client, auth_headers, test_product):
    """Test creating an order"""
    order_data = {
        "customer_name": "John Doe",
        "customer_email": "john@example.com",
        "customer_phone": "555-1234",
        "customer_address": "123 Main St, City, State 12345",
        "items": [{"product_id": test_product["id"], "quantity": 2}],
    }
    response = client.post("/orders", json=order_data, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == order_data["customer_name"]
    assert data["customer_email"] == order_data["customer_email"]
    assert data["status"] == "pending"
    assert data["total_amount"] == test_product["price"] * 2
    assert "id" in data


def test_create_order_with_items(client, auth_headers, test_product):
    """Test that created order includes items"""
    order_data = {
        "customer_name": "Jane Doe",
        "customer_email": "jane@example.com",
        "customer_address": "456 Oak St, City, State 12345",
        "items": [{"product_id": test_product["id"], "quantity": 3}],
    }
    response = client.post("/orders", json=order_data, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == test_product["id"]
    assert data["items"][0]["quantity"] == 3


def test_create_order_reduces_stock(client, auth_headers, test_product):
    """Test that creating an order reduces product stock"""
    initial_stock = test_product["stock"]
    order_quantity = 5

    order_data = {
        "customer_name": "Stock Tester",
        "customer_email": "stock@example.com",
        "customer_address": "789 Elm St, City, State 12345",
        "items": [{"product_id": test_product["id"], "quantity": order_quantity}],
    }
    response = client.post("/orders", json=order_data, headers=auth_headers)
    assert response.status_code == 201

    # Check product stock was reduced
    product_response = client.get(f"/products/{test_product['id']}")
    updated_product = product_response.json()
    assert updated_product["stock"] == initial_stock - order_quantity


def test_create_order_insufficient_stock(client, auth_headers, test_product):
    """Test that order fails when insufficient stock"""
    order_data = {
        "customer_name": "Greedy Customer",
        "customer_email": "greedy@example.com",
        "customer_address": "999 Fail St, City, State 12345",
        "items": [
            {"product_id": test_product["id"], "quantity": 99999}  # More than available
        ],
    }
    response = client.post("/orders", json=order_data, headers=auth_headers)

    assert response.status_code == 400
    assert "insufficient stock" in response.json()["detail"].lower()


def test_create_order_nonexistent_product(client, auth_headers):
    """Test that order fails with nonexistent product"""
    order_data = {
        "customer_name": "Bad Order",
        "customer_email": "bad@example.com",
        "customer_address": "000 Error St, City, State 12345",
        "items": [{"product_id": 99999, "quantity": 1}],
    }
    response = client.post("/orders", json=order_data, headers=auth_headers)

    assert response.status_code == 400
    assert "not found" in response.json()["detail"].lower()


def test_get_all_orders(client, auth_headers, test_product):
    """Test getting all orders"""
    # Create an order first
    order_data = {
        "customer_name": "Test Customer",
        "customer_email": "customer@example.com",
        "customer_address": "123 Test St, City, State 12345",
        "items": [{"product_id": test_product["id"], "quantity": 1}],
    }
    client.post("/orders", json=order_data, headers=auth_headers)

    response = client.get("/orders")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_order_by_id(client, auth_headers, test_product):
    """Test getting a specific order"""
    # Create an order
    order_data = {
        "customer_name": "Specific Customer",
        "customer_email": "specific@example.com",
        "customer_address": "456 Specific St, City, State 12345",
        "items": [{"product_id": test_product["id"], "quantity": 2}],
    }
    create_response = client.post("/orders", json=order_data, headers=auth_headers)
    order_id = create_response.json()["id"]

    response = client.get(f"/orders/{order_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["customer_name"] == order_data["customer_name"]
    assert len(data["items"]) == 1


def test_update_order_status(client, auth_headers, test_product):
    """Test updating order status"""
    # Create an order
    order_data = {
        "customer_name": "Status Update Customer",
        "customer_email": "status@example.com",
        "customer_address": "789 Status St, City, State 12345",
        "items": [{"product_id": test_product["id"], "quantity": 1}],
    }
    create_response = client.post("/orders", json=order_data, headers=auth_headers)
    order_id = create_response.json()["id"]

    # Update status
    response = client.patch(
        f"/orders/{order_id}/status", json={"status": "shipped"}, headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "shipped"


def test_cancel_order(client, auth_headers, test_product):
    """Test canceling an order"""
    initial_stock = test_product["stock"]

    # Create an order
    order_data = {
        "customer_name": "Cancel Customer",
        "customer_email": "cancel@example.com",
        "customer_address": "111 Cancel St, City, State 12345",
        "items": [{"product_id": test_product["id"], "quantity": 3}],
    }
    create_response = client.post("/orders", json=order_data, headers=auth_headers)
    order_id = create_response.json()["id"]

    # Cancel the order
    response = client.delete(f"/orders/{order_id}/cancel", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "cancelled"

    # Verify stock was restored
    product_response = client.get(f"/products/{test_product['id']}")
    updated_product = product_response.json()
    assert updated_product["stock"] == initial_stock


def test_filter_orders_by_status(client, auth_headers, test_product):
    """Test filtering orders by status"""
    # Create orders with different statuses
    for i in range(3):
        order_data = {
            "customer_name": f"Customer {i}",
            "customer_email": f"customer{i}@example.com",
            "customer_address": f"{i} Test St, City, State 12345",
            "items": [{"product_id": test_product["id"], "quantity": 1}],
        }
        client.post("/orders", json=order_data, headers=auth_headers)

    response = client.get("/orders/filter?status=pending")

    assert response.status_code == 200
    data = response.json()
    assert all(order["status"] == "pending" for order in data)
