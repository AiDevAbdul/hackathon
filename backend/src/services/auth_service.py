from datetime import datetime, timedelta
from typing import Optional
import uuid
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.user import User
from ..config.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a plain password."""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password."""
        result = await db.execute(select(User).filter(User.email == email))
        user = result.scalar_one_or_none()

        if not user or not AuthService.verify_password(password, user.password_hash):
            return None

        # Update last login time
        user.last_login = datetime.utcnow()
        db.add(user)
        await db.commit()

        return user

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get a user by email."""
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(
        db: AsyncSession,
        email: str,
        password: str,
        name: str,
        role: str = "student",
        background_software: Optional[str] = None,
        background_hardware: Optional[str] = None
    ) -> User:
        """Create a new user with hashed password."""
        hashed_password = AuthService.get_password_hash(password)
        user = User(
            id=uuid.uuid4(),
            email=email,
            password_hash=hashed_password,
            name=name,
            role=role,
            background_software=background_software,
            background_hardware=background_hardware
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user