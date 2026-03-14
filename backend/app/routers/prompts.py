from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.prompt_service import PromptService, get_prompt_service

router = APIRouter()

class PromptPayload(BaseModel):
    text: str

@router.post("/generate-prompt")
async def generate_prompt(
    payload: PromptPayload,
    prompt_service: PromptService = Depends(get_prompt_service)
):
    optimized_text = await prompt_service.generate_optimized_prompt(payload.text)
    return {"received_text": payload.text, "optimized_text": optimized_text, "status": "ok"}
