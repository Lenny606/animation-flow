from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class CustomPrompt(BaseModel):
    id: Optional[str] = Field(None, alias="_id", description="MongoDB ID")
    name: str = Field(..., description="Unique identifier for the prompt, e.g., 'story_outline'")
    template_text: str = Field(..., description="The prompt template content")
    version: int = Field(1, description="Version number of the prompt")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "story_outline",
                "template_text": "Write a story about {topic} in {style} style.",
                "version": 1
            }
        }
