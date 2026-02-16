from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ImageData(BaseModel):
    id: Optional[str] = Field(None, alias="_id", description="MongoDB ID")
    filename: str = Field(..., description="Name of the file")
    title: str = Field(..., description="Title of the image")
    description: Optional[str] = Field(None, description="Description of the image")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "filename": "sunset.jpg",
                "title": "Beautiful Sunset",
                "description": "A photo of a sunset over the ocean.",
            }
        }
