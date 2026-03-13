from fastapi import APIRouter, HTTPException, Depends, status, Request
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
import json
import redis.asyncio as redis

from app.models.asset import ImageAsset, VideoAsset
from app.db.redis import get_redis
from app.repositories.asset_repository import VideoAssetRepository, get_video_asset_repository
from app.core.error_handling import NotFoundException, ForbiddenException, InternalServerException
from app.core.rate_limit import limiter, get_role_limit
from app.core.security import get_current_user

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

class VideoGenRequest(BaseModel):
    scenario_id: str = Field(..., description="The ID of the scenario the video is based on", examples=["60d5ecb8b392d011f8871123"])
    image_assets: List[ImageAsset] = Field(..., description="The list of image assets to animate")
    provider: str = Field("mock", description="The video generation provider to use", examples=["runway", "luma", "mock"])
    generate_voiceover: bool = Field(False, description="Whether to also generate a voiceover for the video", examples=[True])

class VideoExecuteRequest(BaseModel):
    plan_id: str = Field(..., description="The unique ID of the previously generated video plan", examples=["80d1964f-4795-4672-911e-45041a733739"])

class VideoPlanResponse(BaseModel):
    plan_id: str = Field(..., description="The unique ID of the generated video plan", examples=["80d1964f-4795-4672-911e-45041a733739"])
    script: List[str] = Field(..., description="A step-by-step description of the planned generation process", examples=[["Generate video for image 1", "Generate voiceover"]])

@router.post("/plan", response_model=VideoPlanResponse, summary="Create a video generation plan", description="Initializes the video generation process by creating a plan. Returns a plan ID that must be used to execute the generation.")
@limiter.limit(get_role_limit("3/minute", "10/minute", "60/minute"))
async def generate_video_plan(
    request: Request,
    video_request: VideoGenRequest, 
    redis_conn: redis.Redis = Depends(get_redis),
    current_user: dict = Depends(get_current_user)
):
    """
    Step 1: Generates a plan (script) for video generation and saves it to Redis.
    """
    raise HTTPException(status_code=501, detail="Video plan endpoint is disabled due to AI Agent removal. Not Implemented.")

@router.post("/execute", response_model=List[VideoAsset], summary="Execute a video plan", description="Executes a previously created video generation plan. This is where the actual (time-consuming) generation happens.")
@limiter.limit(get_role_limit("2/minute", "5/minute", "30/minute"))
async def execute_video_plan(
    request: Request,
    execute_request: VideoExecuteRequest, 
    redis_conn: redis.Redis = Depends(get_redis),
    video_repo: VideoAssetRepository = Depends(get_video_asset_repository),
    current_user: dict = Depends(get_current_user)
):
    """
    Step 2: Executes a previously confirmed video generation plan.
    Saves the generated video assets to the database.
    """
    raise HTTPException(status_code=501, detail="Video execution endpoint is disabled due to AI Agent removal. Not Implemented.")
