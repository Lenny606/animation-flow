from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import Optional
from pydantic import BaseModel

from app.models.scenario import Scenario
from app.core.agent.graph import scenario_agent

router = APIRouter(
    prefix="/scenarios",
    tags=["scenarios"],
    responses={404: {"description": "Not found"}},
)

class GenerateScenarioRequest(BaseModel):
    topic: str
    style: str
    target_audience: str = "General Audience"
    duration: int = 60
    llm_provider: str = "openai"

@router.post("/generate", response_model=Scenario)
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

@router.get("/{id}", response_model=Scenario)
async def get_scenario(id: str):
    raise HTTPException(status_code=501, detail="Not implemented yet via DB")
