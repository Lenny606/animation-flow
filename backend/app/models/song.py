from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Song(BaseModel):
    id: Optional[str] = Field(None, alias="_id", description="MongoDB ID")
    title: str = Field(..., description="Title of the song")
    text: str = Field(..., description="Lyrics of the song")
    playlist_name: str = Field(..., description="Name of the playlist this song belongs to")
    category: str = Field(..., description="Category of the song")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "title": "Komáři se ženili",
                "text": "1. Komáři se ženili...",
                "playlist_name": "Klasické české lidové písničky",
                "category": "Lidová tvorba"
            }
        }
