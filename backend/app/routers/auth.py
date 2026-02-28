from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.config import get_settings
from app.core.security import verify_password, create_access_token, get_password_hash
from app.models.user import UserCreate, User, UserInDB, UserLogin
from typing import Annotated
from app.core.error_handling import ConflictException, UnauthorizedException
from app.repositories.user_repository import UserRepository, get_user_repository

settings = get_settings()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")

@router.post("/register", response_model=User, summary="Register a new user", description="Creates a new user account with the provided email and password.")
async def register(user: UserCreate, user_repo: UserRepository = Depends(get_user_repository)):
    existing_user = await user_repo.get_by_email(user.email)
    if existing_user:
        raise ConflictException(detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(email=user.email, hashed_password=hashed_password, role=user.role)
    
    created_user = await user_repo.create(user_in_db)
    return created_user

@router.post("/signup", response_model=User, summary="User signup", description="Alias for /register. Creates a new user account.")
async def signup(user: UserCreate, user_repo: UserRepository = Depends(get_user_repository)):
    return await register(user, user_repo)

@router.post("/login", summary="Login", description="Authenticates a user and returns an access token.")
async def login(user_login: UserLogin, user_repo: UserRepository = Depends(get_user_repository)):
    user = await user_repo.get_by_email(user_login.email)
    if not user or not verify_password(user_login.password, user.hashed_password):
        raise UnauthorizedException(detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", summary="Token exchange (OAuth2)", description="Authenticates a user and returns an access token. Used by OAuth2 compatible clients.")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repo: UserRepository = Depends(get_user_repository)
):
    user = await user_repo.get_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise UnauthorizedException(detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
