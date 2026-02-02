import pytest
from models import Patient, LabOrder, Result


class TestPatients:
    def test_list_patients_empty(self, client):
        """Test listing patients when none exist."""
        response = client.get("/patients/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_patient_with_auth(self, client, auth_headers):
        """Test creating a patient with proper auth."""
        headers = auth_headers()
        response = client.post(
            "/patients/",
            json={"first_name": "Alice", "last_name": "Brown", "dob": "1985-05-20"},
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Alice"
        assert data["last_name"] == "Brown"
        assert data["id"] is not None

    def test_create_patient_validation(self, client, auth_headers):
        """Test that patient creation validates input."""
        headers = auth_headers()
        response = client.post(
            "/patients/",
            json={"first_name": "", "last_name": "Doe"},  # Empty first_name
            headers=headers
        )
        assert response.status_code == 422  # Validation error

    def test_list_patients_after_create(self, client, auth_headers):
        """Test listing patients after creating some."""
        headers = auth_headers()
        # Create patient
        client.post(
            "/patients/",
            json={"first_name": "Charlie", "last_name": "Davis"},
            headers=headers
        )
        # List
        response = client.get("/patients/")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["first_name"] == "Charlie"

    def test_get_patient_by_id(self, client, auth_headers):
        """Test fetching a single patient by ID."""
        headers = auth_headers()
        # Create
        create_response = client.post(
            "/patients/",
            json={"first_name": "Diana", "last_name": "Evans"},
            headers=headers
        )
        patient_id = create_response.json()["id"]
        # Get
        response = client.get(f"/patients/{patient_id}")
        assert response.status_code == 200
        assert response.json()["first_name"] == "Diana"

    def test_get_patient_not_found(self, client):
        """Test getting a nonexistent patient."""
        response = client.get("/patients/999")
        assert response.status_code == 404


class TestLabOrders:
    def test_create_order_with_auth(self, client, auth_headers):
        """Test creating a lab order."""
        headers = auth_headers()
        # Create patient first
        p_res = client.post(
            "/patients/",
            json={"first_name": "Frank", "last_name": "Garcia"},
            headers=headers
        )
        patient_id = p_res.json()["id"]
        # Create order
        response = client.post(
            "/orders/",
            json={"patient_id": patient_id, "test_name": "Blood Test"},
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["test_name"] == "Blood Test"
        assert data["patient_id"] == patient_id

    def test_create_order_invalid_patient(self, client, auth_headers):
        """Test creating order with nonexistent patient."""
        headers = auth_headers()
        response = client.post(
            "/orders/",
            json={"patient_id": 999, "test_name": "Blood Test"},
            headers=headers
        )
        # Should fail on DB constraint
        assert response.status_code != 200

    def test_list_orders(self, client, auth_headers):
        """Test listing lab orders."""
        headers = auth_headers()
        response = client.get("/orders/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestResults:
    def test_create_result_with_auth(self, client, auth_headers):
        """Test creating a test result."""
        headers = auth_headers()
        # Create patient and order
        p_res = client.post(
            "/patients/",
            json={"first_name": "Grace", "last_name": "Harris"},
            headers=headers
        )
        patient_id = p_res.json()["id"]
        o_res = client.post(
            "/orders/",
            json={"patient_id": patient_id, "test_name": "Glucose Test"},
            headers=headers
        )
        order_id = o_res.json()["id"]
        # Create result
        response = client.post(
            "/results/",
            json={"order_id": order_id, "value": "Normal"},
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["value"] == "Normal"
        assert data["order_id"] == order_id

    def test_list_results(self, client):
        """Test listing results."""
        response = client.get("/results/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
