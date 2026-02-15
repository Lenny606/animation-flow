from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional

from app.core.agent.image_agent import image_agent
from app.models.scenario import Scenario
from app.models.asset import ImageAsset

# Mock DB for MVP till generic DB layer is fully plugged
# In real app, we would inject the DB service
from app.routers.scenarios import generate_scenario # just for types, not usage

router = APIRouter(
    prefix="/assets",
    tags=["assets"],
    responses={404: {"description": "Not found"}},
)

class ImageGenRequest(BaseModel):
    scenario: dict # Pass the full scenario object for now to avoid DB lookup complexity in MVP
    llm_provider: str = "openai" # For the planning phase

@router.post("/generate_from_scenario", response_model=List[dict])
async def generate_assets(request: ImageGenRequest):
    """
    Triggers the Image Agent to generate assets for a given scenario.
    Returns the list of generated assets.
    """
    try:
        inputs = {
            "scenario": request.scenario,
            "provider": request.llm_provider
        }
        
        # Ainvoke the agent
        result = await image_agent.ainvoke(inputs)
        
        assets = result.get("generated_assets", [])
        
        # TODO: Batch insert into DB
        
        return assets
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
