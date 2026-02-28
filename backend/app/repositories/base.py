from typing import Generic, TypeVar, Type, List, Optional, Any, Union
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from pydantic import BaseModel
from bson import ObjectId

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str, model_type: Type[T]):
        self.db = db
        self.collection: AsyncIOMotorCollection = db[collection_name]
        self.model_type = model_type

    async def create(self, obj_in: Union[T, dict, Any]) -> T:
        if isinstance(obj_in, dict):
            obj_data = obj_in
        elif hasattr(obj_in, "model_dump"):
            obj_data = obj_in.model_dump(by_alias=True, exclude={"id"})
        else:
            # Fallback for other types if any
            obj_data = dict(obj_in)
        
        result = await self.collection.insert_one(obj_data)
        created_obj = await self.collection.find_one({"_id": result.inserted_id})
        return self._map_to_model(created_obj)

    async def get(self, id: str) -> Optional[T]:
        if not ObjectId.is_valid(id):
            return None
        obj = await self.collection.find_one({"_id": ObjectId(id)})
        return self._map_to_model(obj)

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[T]:
        cursor = self.collection.find().skip(skip).limit(limit)
        results = await cursor.to_list(length=limit)
        return [self._map_to_model(item) for item in results]

    async def update(self, id: str, obj_in: Union[T, dict, Any]) -> Optional[T]:
        if not ObjectId.is_valid(id):
            return None
        
        if isinstance(obj_in, dict):
            update_data = obj_in
        elif hasattr(obj_in, "model_dump"):
            update_data = obj_in.model_dump(exclude_unset=True, by_alias=True, exclude={"id"})
        else:
            update_data = dict(obj_in)
            
        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        return await self.get(id)

    async def delete(self, id: str) -> bool:
        if not ObjectId.is_valid(id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

    def _map_to_model(self, data: Optional[dict]) -> Optional[T]:
        if data is None:
            return None
        # Convert _id to id for Pydantic models
        if "_id" in data:
            data["id"] = str(data.pop("_id"))
        return self.model_type(**data)
