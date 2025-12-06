import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime
import sys
import os

# Add the backend src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.src.main import app
from backend.src.database import get_db, Base
from backend.src.models.user import User
from backend.src.services.auth_service import AuthService


# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False}  # Required for SQLite in-memory
)

# Create a session factory
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


# Override the get_db dependency
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


# Apply the override
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    """Create a test client for the API"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module", autouse=True)
async def setup_db():
    """Set up the test database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Cleanup can be done here if needed


class TestAuth:
    """Test cases for authentication functionality"""

    def test_user_registration(self, client):
        """Test user registration functionality"""
        # Test data for registration
        registration_data = {
            "email": "test@example.com",
            "password": "securepassword123",
            "name": "Test User",
            "background_software": "Software Developer",
            "background_hardware": "Robotics Hobbyist"
        }

        # Make registration request
        response = client.post("/auth/register", json=registration_data)

        # Verify response
        assert response.status_code == 200
        response_data = response.json()
        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"
        print("✓ User registration test passed")

    def test_user_registration_with_invalid_email(self, client):
        """Test user registration with invalid email format"""
        # Test data with invalid email
        registration_data = {
            "email": "invalid-email",
            "password": "securepassword123",
            "name": "Test User",
            "background_software": "Software Developer",
            "background_hardware": "Robotics Hobbyist"
        }

        # Make registration request
        response = client.post("/auth/register", json=registration_data)

        # Should return validation error
        assert response.status_code == 422  # Unprocessable Entity
        print("✓ User registration validation test passed")

    def test_user_registration_duplicate_email(self, client):
        """Test user registration with duplicate email"""
        # First registration
        registration_data = {
            "email": "duplicate@example.com",
            "password": "securepassword123",
            "name": "Test User",
            "background_software": "Software Developer",
            "background_hardware": "Robotics Hobbyist"
        }

        # First registration should succeed
        response = client.post("/auth/register", json=registration_data)
        assert response.status_code == 200

        # Second registration with same email should fail
        response = client.post("/auth/register", json=registration_data)
        assert response.status_code == 409  # Conflict
        print("✓ User registration duplicate email test passed")

    def test_user_login(self, client):
        """Test user login functionality"""
        # First, register a user
        registration_data = {
            "email": "login@example.com",
            "password": "securepassword123",
            "name": "Login User",
            "background_software": "Software Developer",
            "background_hardware": "Robotics Hobbyist"
        }

        # Register the user
        response = client.post("/auth/register", json=registration_data)
        assert response.status_code == 200

        # Now try to login
        login_data = {
            "email": "login@example.com",
            "password": "securepassword123"
        }

        response = client.post("/auth/login", json=login_data)

        # Verify response
        assert response.status_code == 200
        response_data = response.json()
        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"
        print("✓ User login test passed")

    def test_user_login_invalid_credentials(self, client):
        """Test user login with invalid credentials"""
        # Try to login with non-existent user
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }

        response = client.post("/auth/login", json=login_data)

        # Should return unauthorized
        assert response.status_code == 401
        print("✓ User login invalid credentials test passed")

    def test_user_login_wrong_password(self, client):
        """Test user login with wrong password"""
        # First, register a user
        registration_data = {
            "email": "wrongpass@example.com",
            "password": "correctpassword123",
            "name": "Wrong Password User",
            "background_software": "Software Developer",
            "background_hardware": "Robotics Hobbyist"
        }

        # Register the user
        response = client.post("/auth/register", json=registration_data)
        assert response.status_code == 200

        # Now try to login with wrong password
        login_data = {
            "email": "wrongpass@example.com",
            "password": "wrongpassword123"
        }

        response = client.post("/auth/login", json=login_data)

        # Should return unauthorized
        assert response.status_code == 401
        print("✓ User login wrong password test passed")

    def test_get_current_user(self, client):
        """Test getting current user with valid token"""
        # First, register and login to get a token
        registration_data = {
            "email": "currentuser@example.com",
            "password": "securepassword123",
            "name": "Current User",
            "background_software": "Software Developer",
            "background_hardware": "Robotics Hobbyist"
        }

        # Register the user
        response = client.post("/auth/register", json=registration_data)
        assert response.status_code == 200
        token_data = response.json()
        access_token = token_data["access_token"]

        # Now make request to get current user
        response = client.get("/auth/me", headers={"Authorization": f"Bearer {access_token}"})

        # Verify response
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["email"] == "currentuser@example.com"
        assert user_data["name"] == "Current User"
        print("✓ Get current user test passed")

    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token"""
        # Make request with invalid token
        response = client.get("/auth/me", headers={"Authorization": "Bearer invalid_token"})

        # Should return unauthorized
        assert response.status_code == 401
        print("✓ Get current user invalid token test passed")


def run_tests():
    """Run all authentication tests"""
    print("Running authentication tests...")

    # Create a test client
    with TestClient(app) as test_client:
        # Run the tests
        test_instance = TestAuth()

        # Create the database tables
        asyncio.run(setup_db())

        # Run each test
        test_instance.test_user_registration(test_client)
        test_instance.test_user_registration_with_invalid_email(test_client)
        test_instance.test_user_registration_duplicate_email(test_client)
        test_instance.test_user_login(test_client)
        test_instance.test_user_login_invalid_credentials(test_client)
        test_instance.test_user_login_wrong_password(test_client)
        test_instance.test_get_current_user(test_client)
        test_instance.test_get_current_user_invalid_token(test_client)

    print("\n✅ All authentication tests passed!")


if __name__ == "__main__":
    run_tests()