from fastapi import APIRouter, BackgroundTasks, Depends, status, HTTPException
from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.scenario import Scenario
from app.core.error_handling import BaseAPIException, NotFoundException, InternalServerException
from app.repositories.scenario_repository import ScenarioRepository, get_scenario_repository

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

class GenerateScenarioRequest(BaseModel):
    topic: str = Field(..., description="The main topic of the video", examples=["Artificial Intelligence"])
    style: str = Field(..., description="The visual style of the video", examples=["Cinematic sci-fi"])
    target_audience: str = Field("General Audience", description="The intended audience", examples=["Tech enthusiasts"])
    duration: int = Field(60, description="The desired duration of the video in seconds", examples=[30])
    llm_provider: str = Field("openai", description="The LLM provider to use for generation", examples=["openai", "anthropic"])
    thread_id: Optional[str] = Field(None, description="The LangGraph thread ID for state persistence", examples=["some-unique-thread-id"])

@router.post("/generate", response_model=Scenario, summary="Generate a scenario", description="Triggers the AI agent to generate a detailed video scenario based on a topic and style.")
async def generate_scenario(
    request: GenerateScenarioRequest,
    scenario_repo: ScenarioRepository = Depends(get_scenario_repository)
):
    """
    Trigger the AI agent to generate a video scenario and save it to the database.
    """
    raise HTTPException(status_code=501, detail="AI Agent logic has been removed. Not Implemented.")

@router.get("/", response_model=List[Scenario], summary="List scenarios", description="Retrieves a list of all scenarios.")
async def list_scenarios(
    skip: int = 0,
    limit: int = 100,
    scenario_repo: ScenarioRepository = Depends(get_scenario_repository)
):
    return await scenario_repo.get_multi(skip=skip, limit=limit)

@router.get("/{id}", response_model=Scenario, summary="Get scenario by ID", description="Retrieves a specific scenario by its unique identifier.")
async def get_scenario(
    id: str,
    scenario_repo: ScenarioRepository = Depends(get_scenario_repository)
):
    scenario = await scenario_repo.get(id)
    if not scenario:
        raise NotFoundException(detail=f"Scenario with ID {id} not found")
    return scenario

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete scenario", description="Deletes a specific scenario.")
async def delete_scenario(
    id: str,
    scenario_repo: ScenarioRepository = Depends(get_scenario_repository)
):
    success = await scenario_repo.delete(id)
    if not success:
        raise NotFoundException(detail=f"Scenario with ID {id} not found")

