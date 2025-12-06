from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr
from jose import jwt, JWTError

# Import rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

from ..database import get_db
from ..models.user import User
from ..services.auth_service import AuthService
from ..config.settings import settings

# Initialize limiter for this router
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    background_software: str = None
    background_hardware: str = None

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    background_software: str = None
    background_hardware: str = None
    created_at: str
    updated_at: str
    last_login: str = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class CurrentUserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    background_software: str = None
    background_hardware: str = None

@router.post("/register", response_model=TokenResponse)
@limiter.limit("10/hour")  # Limit registration attempts to prevent spam
async def register_user(
    user_data: UserRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    # Check if user already exists
    existing_user = await AuthService.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create new user
    user = await AuthService.create_user(
        db=db,
        email=user_data.email,
        password=user_data.password,
        name=user_data.name,
        background_software=user_data.background_software,
        background_hardware=user_data.background_hardware
    )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")  # Limit login attempts to prevent brute force
async def login_user(
    user_data: UserLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    user = await AuthService.authenticate_user(
        db, user_data.email, user_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=CurrentUserResponse)
async def get_current_user(
    current_user: User = Depends(get_current_user)
):
    return CurrentUserResponse(
        id=str(current_user.id),
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
        background_software=current_user.background_software,
        background_hardware=current_user.background_hardware
    )


# Dependency to get current user from token
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await AuthService.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user