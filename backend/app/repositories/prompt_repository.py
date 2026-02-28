from app.repositories.base import BaseRepository
from app.models.prompt_template import CustomPrompt
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
from app.db.mongodb import get_database
from typing import Optional

class PromptRepository(BaseRepository[CustomPrompt]):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "prompts", CustomPrompt)

    async def get_by_name(self, name: str) -> Optional[CustomPrompt]:
        item = await self.collection.find_one({"name": name})
        return self._map_to_model(item)

async def get_prompt_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> PromptRepository:
    return PromptRepository(db)
