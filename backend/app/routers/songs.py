from fastapi import APIRouter, Depends, status
from typing import List, Optional
from app.models.song import Song
from app.repositories.song_repository import SongRepository, get_song_repository
from app.core.error_handling import NotFoundException, InternalServerException

router = APIRouter()

@router.get("/", response_model=List[Song], summary="Get all songs", description="Retrieves a list of all songs available in the database.")
async def get_songs(
    skip: int = 0,
    limit: int = 100,
    song_repo: SongRepository = Depends(get_song_repository)
):
    """
    Get all saved songs.
    """
    try:
        return await song_repo.get_multi(skip=skip, limit=limit)
    except Exception as e:
        raise InternalServerException(detail=f"Failed to retrieve songs: {str(e)}")

@router.get("/category/{category}", response_model=List[Song])
async def get_songs_by_category(
    category: str,
    skip: int = 0,
    limit: int = 100,
    song_repo: SongRepository = Depends(get_song_repository)
):
    return await song_repo.get_by_category(category, skip=skip, limit=limit)

@router.get("/{id}", response_model=Song)
async def get_song(
    id: str,
    song_repo: SongRepository = Depends(get_song_repository)
):
    song = await song_repo.get(id)
    if not song:
        raise NotFoundException(detail="Song not found")
    return song

@router.post("/", response_model=Song, status_code=status.HTTP_201_CREATED)
async def create_song(
    song: Song,
    song_repo: SongRepository = Depends(get_song_repository)
):
    return await song_repo.create(song)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_song(
    id: str,
    song_repo: SongRepository = Depends(get_song_repository)
):
    success = await song_repo.delete(id)
    if not success:
        raise NotFoundException(detail="Song not found")
