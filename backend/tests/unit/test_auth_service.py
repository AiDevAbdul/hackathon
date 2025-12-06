import pytest
import os
import sys
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio
from pydantic import BaseModel

# Add the backend src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.src.services.auth_service import AuthService
from backend.src.models.user import User


class MockDBSession:
    """Mock database session for testing"""
    def __init__(self):
        self.added_objects = []
        self.users = {}  # email -> user mapping for testing
        self.commit_called = False
        self.refresh_called = False

    async def commit(self):
        self.commit_called = True

    async def refresh(self, obj):
        self.refresh_called = True

    def add(self, obj):
        self.added_objects.append(obj)
        if isinstance(obj, User):
            self.users[obj.email] = obj


class MockUser:
    """Mock user object for testing"""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 'test_id')
        self.email = kwargs.get('email', 'test@example.com')
        self.password_hash = kwargs.get('password_hash', 'hashed_password')
        self.name = kwargs.get('name', 'Test User')
        self.role = kwargs.get('role', 'user')
        self.background_software = kwargs.get('background_software', 'Software Developer')
        self.background_hardware = kwargs.get('background_hardware', 'Robotics Hobbyist')
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())
        self.last_login = kwargs.get('last_login', None)
        self.is_active = kwargs.get('is_active', True)

    def __eq__(self, other):
        return isinstance(other, MockUser) and self.email == other.email


class TestAuthService:
    """Test cases for authentication service functionality"""

    @pytest.mark.asyncio
    async def test_create_access_token(self):
        """Test creating an access token"""
        # Test data
        data = {"sub": "test_user_id", "email": "test@example.com"}
        expires_delta = timedelta(minutes=30)

        # Call the function
        token = AuthService.create_access_token(data=data, expires_delta=expires_delta)

        # Verify the token was created (it should be a string)
        assert isinstance(token, str)
        assert len(token) > 0
        print("✓ Create access token test passed")

    @pytest.mark.asyncio
    async def test_verify_password(self):
        """Test password verification"""
        plain_password = "test_password"

        # Create a hashed password using the service
        hashed = AuthService.get_password_hash(plain_password)

        # Verify the password
        result = AuthService.verify_password(plain_password, hashed)

        # Should return True for correct password
        assert result is True

        # Test with wrong password
        wrong_result = AuthService.verify_password("wrong_password", hashed)
        assert wrong_result is False
        print("✓ Password verification test passed")

    @pytest.mark.asyncio
    async def test_get_password_hash(self):
        """Test password hashing"""
        password = "test_password"

        # Create hash
        hashed = AuthService.get_password_hash(password)

        # Should be different from original
        assert hashed != password
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        print("✓ Password hashing test passed")

    @pytest.mark.asyncio
    async def test_create_user(self):
        """Test creating a user"""
        # Create mock database session
        db = MockDBSession()

        # Test data
        email = "newuser@example.com"
        password = "securepassword123"
        name = "New User"

        # Create user
        user = await AuthService.create_user(
            db=db,
            email=email,
            password=password,
            name=name,
            background_software="Software Developer",
            background_hardware="Robotics Enthusiast"
        )

        # Verify user was created
        assert user.email == email
        assert user.name == name
        assert user.background_software == "Software Developer"
        assert user.background_hardware == "Robotics Enthusiast"
        assert user.password_hash != password  # Should be hashed
        assert db.commit_called is True
        assert db.refresh_called is True
        print("✓ Create user test passed")

    @pytest.mark.asyncio
    async def test_get_user_by_email_found(self):
        """Test getting a user by email when user exists"""
        # Create mock database session with a user
        db = MockDBSession()
        existing_user = MockUser(email="existing@example.com")
        db.users["existing@example.com"] = existing_user

        # Get user by email
        user = await AuthService.get_user_by_email(db, "existing@example.com")

        # Verify user was returned
        assert user is not None
        assert user.email == "existing@example.com"
        print("✓ Get user by email (found) test passed")

    @pytest.mark.asyncio
    async def test_get_user_by_email_not_found(self):
        """Test getting a user by email when user doesn't exist"""
        # Create mock database session
        db = MockDBSession()

        # Get user by email that doesn't exist
        user = await AuthService.get_user_by_email(db, "nonexistent@example.com")

        # Verify None was returned
        assert user is None
        print("✓ Get user by email (not found) test passed")

    @pytest.mark.asyncio
    async def test_authenticate_user_success(self):
        """Test authenticating a user with correct credentials"""
        # Create mock database session
        db = MockDBSession()

        # Create a user with hashed password
        email = "authuser@example.com"
        plain_password = "correctpassword"
        hashed_password = AuthService.get_password_hash(plain_password)

        existing_user = MockUser(
            email=email,
            password_hash=hashed_password
        )
        db.users[email] = existing_user

        # Authenticate user
        user = await AuthService.authenticate_user(db, email, plain_password)

        # Verify authentication succeeded
        assert user is not None
        assert user.email == email
        print("✓ User authentication (success) test passed")

    @pytest.mark.asyncio
    async def test_authenticate_user_wrong_password(self):
        """Test authenticating a user with wrong password"""
        # Create mock database session
        db = MockDBSession()

        # Create a user with hashed password
        email = "authuser@example.com"
        plain_password = "correctpassword"
        hashed_password = AuthService.get_password_hash(plain_password)

        existing_user = MockUser(
            email=email,
            password_hash=hashed_password
        )
        db.users[email] = existing_user

        # Authenticate user with wrong password
        user = await AuthService.authenticate_user(db, email, "wrongpassword")

        # Verify authentication failed
        assert user is None
        print("✓ User authentication (wrong password) test passed")

    @pytest.mark.asyncio
    async def test_authenticate_user_nonexistent_user(self):
        """Test authenticating a user that doesn't exist"""
        # Create mock database session
        db = MockDBSession()

        # Authenticate non-existent user
        user = await AuthService.authenticate_user(db, "nonexistent@example.com", "any_password")

        # Verify authentication failed
        assert user is None
        print("✓ User authentication (non-existent user) test passed")


def run_tests():
    """Run all authentication service tests"""
    print("Running authentication service tests...")

    # Create test instance
    test_instance = TestAuthService()

    # Run each test
    asyncio.run(test_instance.test_create_access_token())
    asyncio.run(test_instance.test_verify_password())
    asyncio.run(test_instance.test_get_password_hash())
    asyncio.run(test_instance.test_create_user())
    asyncio.run(test_instance.test_get_user_by_email_found())
    asyncio.run(test_instance.test_get_user_by_email_not_found())
    asyncio.run(test_instance.test_authenticate_user_success())
    asyncio.run(test_instance.test_authenticate_user_wrong_password())
    asyncio.run(test_instance.test_authenticate_user_nonexistent_user())

    print("\n✅ All authentication service tests passed!")


if __name__ == "__main__":
    run_tests()