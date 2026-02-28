from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional

from app.core.agent.image_agent import image_agent
from app.models.scenario import Scenario
from app.models.asset import ImageAsset

# Mock DB for MVP till generic DB layer is fully plugged
# In real app, we would inject the DB service
from app.routers.scenarios import generate_scenario # just for types, not usage

router = APIRouter(
    prefix="/assets",
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
