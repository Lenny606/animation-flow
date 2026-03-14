from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class PromptPayload(BaseModel):
    text: str

@router.post("/generate-prompt")
async def generate_prompt(payload: PromptPayload):
    # This endpoint just receives text and returns it for now, as requested.
    return {"received_text": payload.text, "status": "ok"}
