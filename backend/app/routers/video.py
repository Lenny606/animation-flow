from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.core.agent.video_agent import video_agent
from app.models.asset import ImageAsset, VideoAsset

router = APIRouter(
    prefix="/video",
    tags=["video"],
    responses={404: {"description": "Not found"}},
)

class VideoGenRequest(BaseModel):
    scenario_id: str
    image_assets: List[dict] # Pass full asset dicts for MVP
    provider: str = "mock"
    generate_voiceover: bool = False

@router.post("/generate", response_model=List[dict])
async def generate_video(request: VideoGenRequest):
    """
    Triggers the Video Agent to generate clips from image assets.
    """
    try:
        inputs = {
            "scenario_id": request.scenario_id,
            "image_assets": request.image_assets,
            "provider": request.provider,
            "generate_voiceover": request.generate_voiceover
        }
        
        result = await video_agent.ainvoke(inputs)
        
        assets = result.get("video_assets", [])
        
        return assets
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
