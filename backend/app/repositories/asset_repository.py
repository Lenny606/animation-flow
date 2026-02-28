from app.repositories.base import BaseRepository
from app.models.asset import ImageAsset, VideoAsset
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
from app.db.mongodb import get_database
from typing import List

class ImageAssetRepository(BaseRepository[ImageAsset]):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "image_assets", ImageAsset)

    async def get_by_scenario(self, scenario_id: str) -> List[ImageAsset]:
        cursor = self.collection.find({"scenario_id": scenario_id}).sort("order", 1)
        results = await cursor.to_list(length=100)
        return [self._map_to_model(item) for item in results]

class VideoAssetRepository(BaseRepository[VideoAsset]):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "video_assets", VideoAsset)

    async def get_by_scenario(self, scenario_id: str) -> List[VideoAsset]:
        cursor = self.collection.find({"scenario_id": scenario_id})
        results = await cursor.to_list(length=100)
        return [self._map_to_model(item) for item in results]

async def get_image_asset_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> ImageAssetRepository:
    return ImageAssetRepository(db)

async def get_video_asset_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> VideoAssetRepository:
    return VideoAssetRepository(db)
