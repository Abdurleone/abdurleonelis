import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient
from database import get_session
from models import User
from auth import get_password_hash


@pytest.fixture(name="session")
def session_fixture():
    """Create a test database in memory."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Override the DB session for testing."""
    from main import app
    
    # Pre-create test users in the session
    test_user = User(
        username="testuser",
        hashed_password=get_password_hash("testpass123"),
        role="technician"
    )
    test_admin = User(
        username="adminuser",
        hashed_password=get_password_hash("adminpass123"),
        role="admin"
    )
    session.add(test_user)
    session.add(test_admin)
    session.commit()
    
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    """Create a test user in the session."""
    user = User(
        username="testuser",
        hashed_password=get_password_hash("testpass123"),
        role="technician"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_admin")
def test_admin_fixture(session: Session):
    """Create a test admin user."""
    user = User(
        username="adminuser",
        hashed_password=get_password_hash("adminpass123"),
        role="admin"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(client: TestClient):
    """Helper to get auth headers for a test user."""
    def get_headers(username="testuser", password="testpass123"):
        response = client.post(
            "/auth/token",
            data={"username": username, "password": password}
        )
        if response.status_code != 200:
            raise Exception(f"Failed to get token: {response.json()}")
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    return get_headers
