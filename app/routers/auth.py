from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.security import verify_password, create_access_token, get_password_hash
from app.models.user import UserCreate, User, UserInDB
from app.db.mongodb import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Annotated

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/signup", response_model=User)
async def signup(user: UserCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(email=user.email, hashed_password=hashed_password)
    
    new_user = await db.users.insert_one(user_in_db.model_dump(by_alias=True, exclude={"id"}))
    created_user = await db.users.find_one({"_id": new_user.inserted_id})
    
    # helper to convert _id to id string for response
    created_user["_id"] = str(created_user["_id"])
    return created_user

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    user = await db.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
