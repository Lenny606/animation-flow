from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
import json
import redis.asyncio as redis

from app.core.agent.video_agent import video_agent
from app.models.asset import ImageAsset, VideoAsset
from app.db.redis import get_redis

router = APIRouter(
    prefix="/video",
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
async def generate_video_plan(request: VideoGenRequest, redis_conn: redis.Redis = Depends(get_redis)):
    """
    Step 1: Generates a plan (script) for video generation and saves it to Redis.
    """
    try:
        plan_id = str(uuid.uuid4())
        
        # Generate a simple "script" or plan description
        # In a real agent, this might be an LLM call to decide what to do.
        # For now, we list the actions based on the input images.
        script = []
        for img in request.image_assets:
            prompt = img.get("prompt_used", "Animate this scene")
            script.append(f"Generate video for image {img.get('id', 'unknown')} using prompt: '{prompt}'")
        
        if request.generate_voiceover:
            script.append("Generate voiceover for the video.")

        # Store the full request context in Redis
        plan_data = {
            "request": request.model_dump(),
            "script": script
        }
        
        # Save to Redis with 1 hour expiration
        await redis_conn.setex(f"video_plan:{plan_id}", 3600, json.dumps(plan_data))
        
        return VideoPlanResponse(plan_id=plan_id, script=script)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute", response_model=List[VideoAsset], summary="Execute a video plan", description="Executes a previously created video generation plan. This is where the actual (time-consuming) generation happens.")
async def execute_video_plan(request: VideoExecuteRequest, redis_conn: redis.Redis = Depends(get_redis)):
    """
    Step 2: Executes a previously confirmed video generation plan.
    """
    try:
        # Retrieve plan from Redis
        plan_json = await redis_conn.get(f"video_plan:{request.plan_id}")
        if not plan_json:
            raise HTTPException(status_code=404, detail="Plan not found or expired")
        
        plan_data = json.loads(plan_json)
        original_request = plan_data.get("request")
        
        # Reconstruct inputs for the agent
        inputs = {
            "scenario_id": original_request["scenario_id"],
            "image_assets": original_request["image_assets"],
            "provider": original_request["provider"],
            "generate_voiceover": original_request["generate_voiceover"]
        }
        
        result = await video_agent.ainvoke(inputs)
        
        assets = result.get("video_assets", [])
        
        # Optionally cleanup Redis (or keep it for history/idempotency)
        # await redis_conn.delete(f"video_plan:{request.plan_id}")
        
        return assets
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
