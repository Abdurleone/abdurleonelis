import pytest
from auth import verify_password, get_password_hash, create_access_token
from models import User


class TestPasswordHashing:
    def test_password_hash_creates_different_hash(self):
        """Test that hashing the same password creates different hashes."""
        password = "test123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        # Hashes should be different (due to salt)
        assert hash1 != hash2

    def test_verify_password_correct(self):
        """Test that correct password verifies."""
        password = "mypassword"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test that incorrect password does not verify."""
        password = "mypassword"
        hashed = get_password_hash(password)
        assert verify_password("wrongpassword", hashed) is False


class TestAuth:
    def test_register_user(self, client):
        """Test user registration."""
        response = client.post(
            "/auth/register",
            json={
                "username": "newuser",
                "password": "newpass123",
                "role": "technician"
            }
        )
        assert response.status_code == 200
        assert response.json()["username"] == "newuser"
        assert response.json()["role"] == "technician"

    def test_register_duplicate_username(self, client, test_user):
        """Test that duplicate usernames are rejected."""
        response = client.post(
            "/auth/register",
            json={
                "username": "testuser",
                "password": "anotherpass",
                "role": "admin"
            }
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_login_correct_credentials(self, client, test_user):
        """Test login with correct credentials."""
        response = client.post(
            "/auth/token",
            data={"username": "testuser", "password": "testpass123"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_login_incorrect_password(self, client, test_user):
        """Test login with incorrect password."""
        response = client.post(
            "/auth/token",
            data={"username": "testuser", "password": "wrongpassword"}
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user."""
        response = client.post(
            "/auth/token",
            data={"username": "nouser", "password": "anypass"}
        )
        assert response.status_code == 401


class TestRBAC:
    def test_protected_endpoint_without_token(self, client):
        """Test that protected endpoints require token."""
        response = client.post(
            "/patients/",
            json={"first_name": "John", "last_name": "Doe"}
        )
        assert response.status_code == 401

    def test_technician_can_create_patient(self, client, auth_headers):
        """Test that technician can create patient."""
        headers = auth_headers("testuser", "testpass123")
        response = client.post(
            "/patients/",
            json={"first_name": "Jane", "last_name": "Smith", "dob": "1990-01-15"},
            headers=headers
        )
        assert response.status_code == 200
        assert response.json()["first_name"] == "Jane"

    def test_admin_can_create_patient(self, client, auth_headers):
        """Test that admin can create patient."""
        headers = auth_headers("adminuser", "adminpass123")
        response = client.post(
            "/patients/",
            json={"first_name": "Bob", "last_name": "Johnson"},
            headers=headers
        )
        assert response.status_code == 200

    def test_invalid_token_rejected(self, client):
        """Test that invalid tokens are rejected."""
        response = client.post(
            "/patients/",
            json={"first_name": "John", "last_name": "Doe"},
            headers={"Authorization": "Bearer invalidsignature.token.here"}
        )
        assert response.status_code == 401
