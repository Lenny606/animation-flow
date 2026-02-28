from fastapi import APIRouter, HTTPException, Depends, status, Request
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
import json
import redis.asyncio as redis

from app.core.agent.video_agent import video_agent
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
    try:
        plan_id = str(uuid.uuid4())
        
        # Generate a simple "script" or plan description
        script = []
        for img in video_request.image_assets:
            prompt = img.prompt_used if hasattr(img, 'prompt_used') else img.get("prompt_used", "Animate this scene")
            img_id = img.id if hasattr(img, 'id') else img.get('id', 'unknown')
            script.append(f"Generate video for image {img_id} using prompt: '{prompt}'")
        
        if video_request.generate_voiceover:
            script.append("Generate voiceover for the video.")

        # Store the full request context in Redis
        plan_data = {
            "request": video_request.model_dump(),
            "script": script,
            "user_id": str(current_user.id) if hasattr(current_user, 'id') else None
        }
        
        # Save to Redis with 1 hour expiration
        await redis_conn.setex(f"video_plan:{plan_id}", 3600, json.dumps(plan_data))
        
        return VideoPlanResponse(plan_id=plan_id, script=script)

    except Exception as e:
        raise InternalServerException(detail=f"Failed to generate video plan: {str(e)}")

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
    try:
        # Retrieve plan from Redis
        plan_json = await redis_conn.get(f"video_plan:{execute_request.plan_id}")
        if not plan_json:
            raise NotFoundException(detail="Plan not found or expired")
        
        plan_data = json.loads(plan_json)
        
        # Verify ownership
        if plan_data.get("user_id") and plan_data.get("user_id") != str(current_user.id):
             raise ForbiddenException(detail="Not authorized to execute this plan")

        original_request = plan_data.get("request")
        
        # Reconstruct inputs for the agent
        inputs = {
            "scenario_id": original_request["scenario_id"],
            "image_assets": original_request["image_assets"],
            "provider": original_request["provider"],
            "generate_voiceover": original_request["generate_voiceover"]
        }
        
        result = await video_agent.ainvoke(inputs)
        
        assets_data = result.get("video_assets", [])
        
        # Save to DB and return models
        saved_assets = []
        for asset_data in assets_data:
            saved_asset = await video_repo.create(asset_data)
            saved_assets.append(saved_asset)
        
        return saved_assets
        
    except (NotFoundException, ForbiddenException):
        raise
    except Exception as e:
        raise InternalServerException(detail=f"Failed to execute video plan: {str(e)}")
