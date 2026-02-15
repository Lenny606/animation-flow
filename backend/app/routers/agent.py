from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from pydantic import BaseModel
from app.services.graph import graph
from langchain_core.messages import HumanMessage
from app.routers.auth import oauth2_scheme

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
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
