from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class Scene(BaseModel):
    id: int = Field(..., description="Order/Index of the scene")
    visual_description: str = Field(..., description="Detailed prompt for image generation models")
    voiceover: str = Field(..., description="Script for the narrator to read")
    character_action: Optional[str] = Field(None, description="Specific actions characters take")
    estimated_duration: Optional[int] = Field(None, description="Estimated duration in seconds")

class Scenario(BaseModel):
    id: Optional[str] = Field(None, alias="_id", description="MongoDB ID")
    title: str
    topic: str
    style: str
    target_audience: Optional[str] = None
    scenes: List[Scene]
    llm_provider: str = Field(..., description="The LLM provider used to generate this scenario")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "title": "The Future of AI",
                "topic": "Artificial Intelligence",
                "style": "Cinematic sci-fi",
                "scenes": [
                    {
                        "id": 1,
                        "visual_description": "A glowing neural network hovering in a dark void",
                        "voiceover": "It started with a single spark...",
                        "estimated_duration": 5
                    }
                ],
                "llm_provider": "openai"
            }
        }
