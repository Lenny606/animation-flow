from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.prompt_service import PromptService, get_prompt_service

router = APIRouter()

class PromptPayload(BaseModel):
    song_title: str
    song_text: str
    style: str

@router.post("/generate-prompt")
async def generate_prompt(
    payload: PromptPayload,
    prompt_service: PromptService = Depends(get_prompt_service)
):
    optimized_text = await prompt_service.generate_optimized_prompt(
        payload.song_title, 
        payload.song_text, 
        payload.style
    )
    return {
        "song_title": payload.song_title,
        "style": payload.style,
        "optimized_text": optimized_text, 
        "status": "ok"
    }
