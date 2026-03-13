from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, status
from pydantic import BaseModel, Field
from typing import List, Optional

from app.models.scenario import Scenario
from app.models.asset import ImageAsset, VideoAsset
from app.repositories.asset_repository import (
    ImageAssetRepository, 
    VideoAssetRepository, 
    get_image_asset_repository, 
    get_video_asset_repository
)
from app.core.error_handling import NotFoundException, InternalServerException

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

class ImageGenRequest(BaseModel):
    scenario: dict = Field(..., description="The full scenario object to generate images for", examples=[{
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
    }])
    llm_provider: str = Field("openai", description="The image generation provider to use", examples=["openai", "stabilityai"])

@router.post("/generate_from_scenario", response_model=List[ImageAsset], summary="Generate assets for a scenario", description="Triggers the Image Agent to generate image assets for each scene in a given scenario.")
async def generate_assets(
    request: ImageGenRequest,
    image_repo: ImageAssetRepository = Depends(get_image_asset_repository)
):
    """
    Triggers the Image Agent to generate assets for a given scenario.
    Saves the generated assets to the database.
    """
    raise HTTPException(status_code=501, detail="AI Agent logic has been removed. Not Implemented.")

@router.get("/scenario/{scenario_id}/images", response_model=List[ImageAsset])
async def get_scenario_images(
    scenario_id: str,
    image_repo: ImageAssetRepository = Depends(get_image_asset_repository)
):
    return await image_repo.get_by_scenario(scenario_id)

@router.get("/scenario/{scenario_id}/videos", response_model=List[VideoAsset])
async def get_scenario_videos(
    scenario_id: str,
    video_repo: VideoAssetRepository = Depends(get_video_asset_repository)
):
    return await video_repo.get_by_scenario(scenario_id)

@router.delete("/image/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
    id: str,
    image_repo: ImageAssetRepository = Depends(get_image_asset_repository)
):
    success = await image_repo.delete(id)
    if not success:
        raise NotFoundException(detail="Image asset not found")

@router.delete("/video/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(
    id: str,
    video_repo: VideoAssetRepository = Depends(get_video_asset_repository)
):
    success = await video_repo.delete(id)
    if not success:
        raise NotFoundException(detail="Video asset not found")
