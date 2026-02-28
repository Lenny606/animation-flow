from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from pydantic import BaseModel, Field
from app.services.graph import graph
from langchain_core.messages import HumanMessage
from app.routers.auth import oauth2_scheme

router = APIRouter()

class ChatRequest(BaseModel):
    message: str = Field(..., description="The message to send to the AI agent", examples=["How do I generate a video?"])

class ChatResponse(BaseModel):
    response: str = Field(..., description="The response from the AI agent", examples=["You can start by providing a topic and style for your scenario."])

@router.post("/chat", response_model=ChatResponse, summary="Chat with AI Agent", description="Sends a message to the AI agent and returns its response.")
async def chat(request: ChatRequest, token: str = Depends(oauth2_scheme)):
    # Simple invocation of the graph
    inputs = {"messages": [HumanMessage(content=request.message)]}
    try:
        # invoke is synchronous in this example, but LangGraph supports astream
        # For keeping it simple in skeleton:
        result = await graph.ainvoke(inputs)
        last_message = result["messages"][-1]
        return ChatResponse(response=last_message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
