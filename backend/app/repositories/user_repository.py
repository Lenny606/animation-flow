from typing import Optional
from app.repositories.base import BaseRepository
from app.models.user import UserInDB, User
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
from app.db.mongodb import get_database

class UserRepository(BaseRepository[UserInDB]):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "users", UserInDB)

    async def get_by_email(self, email: str) -> Optional[UserInDB]:
        user = await self.collection.find_one({"email": email})
        return self._map_to_model(user)

async def get_user_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> UserRepository:
    return UserRepository(db)
