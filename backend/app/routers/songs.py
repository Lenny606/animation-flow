from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.db.mongodb import get_database
from app.models.song import Song
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(
    prefix="/songs",
    tags=["songs"],
)

@router.get("/", response_model=List[Song])
async def get_songs(db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Get all saved songs.
    """
    try:
        cursor = db["songs"].find()
        songs = await cursor.to_list(length=100)
        return songs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
