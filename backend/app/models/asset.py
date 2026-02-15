from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ImageAsset(BaseModel):
    id: Optional[str] = Field(None, alias="_id", description="MongoDB ID")
    scenario_id: str = Field(..., description="ID of the parent Scenario")
    prompt_used: str = Field(..., description="The full prompt sent to the image generator")
    image_url: str = Field(..., description="Local path or remote URL of the generated image")
    order: int = Field(..., description="Sequence order of this image in the flow")
    provider: str = Field(..., description="Provider used (e.g., openai-dalle-3)")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "scenario_id": "scen_12345",
                "prompt_used": "A futuristic city with flying cars, neon lights, cyberpunk style...",
                "image_url": "/static/images/scen_12345_1.png",
                "order": 1,
                "provider": "openai-dalle-3"
            }
        }

class VideoAsset(BaseModel):
    id: Optional[str] = Field(None, alias="_id", description="MongoDB ID")
    scenario_id: str = Field(..., description="ID of the parent Scenario")
    image_asset_id: str = Field(..., description="ID of the source image asset")
    video_url: str = Field(..., description="Local path or remote URL of the generated video")
    provider: str = Field(..., description="Provider used (e.g., runway, mock)")
    status: str = Field("pending", description="pending, completed, failed")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "scenario_id": "scen_12345",
                "image_asset_id": "img_123",
                "video_url": "/static/videos/vid_123.mp4",
                "provider": "mock",
                "status": "completed"
            }
        }
