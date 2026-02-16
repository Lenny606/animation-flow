from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ImageData(BaseModel):
    id: Optional[str] = Field(None, alias="_id", description="MongoDB ID")
    filename: str = Field(..., description="Name of the file")
    title: str = Field(..., description="Title of the image")
    description: Optional[str] = Field(None, description="Description of the image")
    medium: Optional[str] = Field(None, description="Medium of the art")
    year: Optional[str] = Field(None, description="Year of creation")
    tags: Optional[list[str]] = Field(None, description="Tags for the image")
    width: Optional[int] = Field(None, description="Width of the image")
    height: Optional[int] = Field(None, description="Height of the image")
    category: Optional[str] = Field(None, description="Category of the image")
    status: Optional[str] = Field(None, description="Status of the image (e.g., available, sold)")
    price: Optional[str] = Field(None, description="Price of the image")
    src: Optional[str] = Field(None, description="Source URL of the image")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "filename": "2024-02-15_12-30-45_cyberpunk-city.png",
                "title": "Neon Horizons",
                "description": "A futuristic cityscape at dusk with flying cars.",
                "medium": "Digital Art",
                "year": "2024",
                "tags": ["cyberpunk", "scifi", "neon"],
                "width": 1024,
                "height": 1024,
                "src": "https://..."
            }
        }
