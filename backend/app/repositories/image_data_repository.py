from app.repositories.base import BaseRepository
from app.models.image_data import ImageData
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
from app.db.mongodb import get_database
from typing import List

class ImageDataRepository(BaseRepository[ImageData]):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "image_data", ImageData)

    async def get_newest_per_filename(self) -> List[ImageData]:
        pipeline = [
            {"$sort": {"created_at": -1}},
            {
                "$group": {
                    "_id": "$filename",
                    "newest_doc": {"$first": "$$ROOT"}
                }
            },
            {"$replaceRoot": {"newRoot": "$newest_doc"}},
            {"$sort": {"created_at": -1}}
        ]
        
        cursor = self.collection.aggregate(pipeline)
        results = await cursor.to_list(length=1000)
        return [self._map_to_model(item) for item in results]

async def get_image_data_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> ImageDataRepository:
    return ImageDataRepository(db)
