from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid
import json
import redis.asyncio as redis

from app.core.agent.video_agent import video_agent
from app.models.asset import ImageAsset, VideoAsset
from app.db.redis import get_redis

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

class VideoExecuteRequest(BaseModel):
    plan_id: str

class VideoPlanResponse(BaseModel):
    plan_id: str
    script: List[str]

@router.post("/plan", response_model=VideoPlanResponse)
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

@router.post("/execute", response_model=List[dict])
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
