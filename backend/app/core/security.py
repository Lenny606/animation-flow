from datetime import datetime, timedelta
from typing import Optional, Union, Annotated
from jose import jwt, JWTError
import bcrypt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from app.core.config import get_settings
from app.models.user import UserInDB, UserRole
from app.repositories.user_repository import UserRepository, get_user_repository
from app.core.error_handling import UnauthorizedException

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/token",
    auto_error=False
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # bcrypt.checkpw requires bytes
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    # bcrypt.hashpw requires bytes and returns bytes
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Add role to token if present in data
    if "role" not in to_encode and "user" in data:
         # Support passing user object
         user = data["user"]
         to_encode["role"] = getattr(user, "role", UserRole.FREE)
         to_encode["sub"] = getattr(user, "email", to_encode.get("sub"))
         del to_encode["user"]
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(
    request: Request,
    token: Annotated[Optional[str], Depends(oauth2_scheme)] = None,
    user_repo: UserRepository = Depends(get_user_repository)
) -> UserInDB:
    if settings.DISABLE_AUTH:
        # Return a mock admin user for local development
        return UserInDB(
            email="admin@example.com",
            hashed_password="mock_password",
            role=UserRole.ADMIN
        )

    if token is None:
        # Try to get token from cookie if not in header
        token = request.cookies.get(settings.AUTH_COOKIE_NAME)
        
    if token is None:
        raise UnauthorizedException(detail="Not authenticated")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise UnauthorizedException(detail="Could not validate credentials")
    except JWTError:
        raise UnauthorizedException(detail="Could not validate credentials")
        
    user = await user_repo.get_by_email(email)
    if user is None:
        raise UnauthorizedException(detail="User not found")
    return user
