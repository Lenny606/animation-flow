from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import Optional
from pydantic import BaseModel, Field

from app.models.scenario import Scenario
from app.core.agent.graph import scenario_agent

router = APIRouter(
    prefix="/scenarios",
    responses={404: {"description": "Not found"}},
)

class GenerateScenarioRequest(BaseModel):
    topic: str = Field(..., description="The main topic of the video", examples=["Artificial Intelligence"])
    style: str = Field(..., description="The visual style of the video", examples=["Cinematic sci-fi"])
    target_audience: str = Field("General Audience", description="The intended audience", examples=["Tech enthusiasts"])
    duration: int = Field(60, description="The desired duration of the video in seconds", examples=[30])
    llm_provider: str = Field("openai", description="The LLM provider to use for generation", examples=["openai", "anthropic"])

@router.post("/generate", response_model=Scenario, summary="Generate a scenario", description="Triggers the AI agent to generate a detailed video scenario based on a topic and style.")
async def generate_scenario(request: GenerateScenarioRequest):
    """
    Trigger the AI agent to generate a video scenario.
    """
    try:
        inputs = {
            "topic": request.topic,
            "style": request.style,
            "target_audience": request.target_audience,
            "duration": request.duration,
            "llm_provider": request.llm_provider
        }
        
        # Invoke the LangGraph agent
        result = await scenario_agent.ainvoke(inputs)
        
        final_data = result.get("final_scenario")
        if not final_data:
            raise HTTPException(status_code=500, detail="Agent failed to produce a final scenario.")
            
        # Convert to Pydantic model (and optionally save to DB here)
        scenario = Scenario(**final_data)
        
        # TODO: Save to MongoDB
        # await db.scenarios.insert_one(scenario.model_dump(by_alias=True))
        
        return scenario
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=Scenario, summary="Get scenario by ID", description="Retrieves a specific scenario by its unique identifier.")
async def get_scenario(id: str):
    raise HTTPException(status_code=501, detail="Not implemented yet via DB")
