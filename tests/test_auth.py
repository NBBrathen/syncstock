def test_register_user(client):
    """Test user registration"""
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "password123",
    }
    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "hashed_password" not in data  # Password should not be returned


def test_register_duplicate_email(client, test_user):
    """Test that duplicate email is rejected"""
    user_data = {
        "email": test_user["email"],  # Same email as test_user
        "username": "differentuser",
        "password": "password123",
    }
    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_register_duplicate_username(client, test_user):
    """Test that duplicate username is rejected"""
    user_data = {
        "email": "different@example.com",
        "username": test_user["username"],  # Same username as test_user
        "password": "password123",
    }
    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 400
    assert "already taken" in response.json()["detail"].lower()


def test_login_success(client, test_user):
    """Test successful login"""
    login_data = {"username": test_user["username"], "password": test_user["password"]}
    response = client.post("/auth/login", data=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    """Test login with wrong password"""
    login_data = {"username": test_user["username"], "password": "wrongpassword"}
    response = client.post("/auth/login", data=login_data)

    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


def test_login_nonexistent_user(client):
    """Test login with nonexistent user"""

    login_data = {"username": "goofyusername222", "password": "password1234"}
    response = client.post("/auth/login", data=login_data)

    assert response.status_code == 401


def test_get_current_user(client, auth_headers):
    """Test getting current user info"""
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_get_current_user_without_token(client):
    """Test that /auth/me requires authentication"""
    response = client.get("/auth/me")

    assert response.status_code == 401
