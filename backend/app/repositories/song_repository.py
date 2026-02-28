from app.repositories.base import BaseRepository
from app.models.song import Song
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
from app.db.mongodb import get_database
from typing import List, Optional

class SongRepository(BaseRepository[Song]):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "songs", Song)

    async def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Song]:
        cursor = self.collection.find({"category": category}).skip(skip).limit(limit)
        results = await cursor.to_list(length=limit)
        return [self._map_to_model(item) for item in results]

    async def get_by_title(self, title: str) -> Optional[Song]:
        item = await self.collection.find_one({"title": title})
        return self._map_to_model(item)

async def get_song_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> SongRepository:
    return SongRepository(db)
