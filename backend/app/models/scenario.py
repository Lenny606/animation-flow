from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class Scene(BaseModel):
    id: int = Field(..., description="Order/Index of the scene", examples=[1])
    visual_description: str = Field(..., description="Detailed prompt for image generation models", examples=["A glowing neural network hovering in a dark void"])
    voiceover: str = Field(..., description="Script for the narrator to read", examples=["It started with a single spark..."])
    character_action: Optional[str] = Field(None, description="Specific actions characters take", examples=["The character looks up in awe"])
    estimated_duration: Optional[int] = Field(None, description="Estimated duration in seconds", examples=[5])

class Scenario(BaseModel):
    id: Optional[str] = Field(None, alias="_id", description="Unique identifier for the scenario (MongoDB ID)", examples=["60d5ecb8b392d011f8871123"])
    title: str = Field(..., description="Title of the scenario", examples=["The Future of AI"])
    topic: str = Field(..., description="Main topic of the video", examples=["Artificial Intelligence"])
    style: str = Field(..., description="Visual style for image generation", examples=["Cinematic sci-fi"])
    target_audience: Optional[str] = Field(None, description="Intended audience for the video", examples=["General Audience"])
    scenes: List[Scene] = Field(..., description="List of scenes that make up the scenario")
    llm_provider: str = Field(..., description="The LLM provider used to generate this scenario", examples=["openai"])
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the scenario was created")

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
