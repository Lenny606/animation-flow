from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import json
from typing import List, Dict, Optional, AsyncGenerator
from pydantic import BaseModel, Field
from app.services.graph import graph
from langchain_core.messages import HumanMessage, BaseMessage
from app.routers.auth import oauth2_scheme
from app.core.error_handling import InternalServerException

router = APIRouter()

class ChatRequest(BaseModel):
    message: str = Field(..., description="The message to send to the AI agent", examples=["How do I generate a video?"])
    thread_id: Optional[str] = Field(None, description="The LangGraph thread ID for state persistence", examples=["user-123-session-456"])

class ChatResponse(BaseModel):
    response: str = Field(..., description="The response from the AI agent", examples=["You can start by providing a topic and style for your scenario."])

async def agent_stream_generator(request: ChatRequest) -> AsyncGenerator[str, None]:
    """
    Generator that streams LLM response chunks as Server-Sent Events (SSE).
    """
    inputs = {"messages": [HumanMessage(content=request.message)]}
    config = {"configurable": {"thread_id": request.thread_id or "default-chat-thread"}}
    
    # Using astream with stream_mode="messages" to get individual message tokens
    async for msg, metadata in graph.astream(inputs, config=config, stream_mode="messages"):
        if isinstance(msg.content, str) and msg.content:
            # Yielding just the content as a string for simplicity, or we could use JSON/SSE format
            yield msg.content

@router.post("/chat", response_model=ChatResponse, summary="Chat with AI Agent", description="Sends a message to the AI agent and returns its response.")
async def chat(request: ChatRequest, token: str = Depends(oauth2_scheme)):
    # Simple invocation of the graph with checkpointer config
    inputs = {"messages": [HumanMessage(content=request.message)]}
    config = {"configurable": {"thread_id": request.thread_id or "default-chat-thread"}}
    try:
        # invoke is synchronous in this example, but LangGraph supports astream
        # For keeping it simple in skeleton:
        result = await graph.ainvoke(inputs, config=config)
        last_message = result["messages"][-1]
        return ChatResponse(response=last_message.content)
    except Exception as e:
        raise InternalServerException(detail=f"Agent interaction failed: {str(e)}")

@router.post("/chat/stream", summary="Stream Chat with AI Agent", description="Streams the AI agent's response chunk by chunk.")
async def chat_stream(request: ChatRequest, token: str = Depends(oauth2_scheme)):
    """
    Streams the AI agent's response using StreamingResponse.
    """
    return StreamingResponse(
        agent_stream_generator(request),
        media_type="text/event-stream"
    )

@router.get("/{thread_id}/state", summary="Get chat agent state by thread ID")
async def get_chat_state(thread_id: str):
    """
    Retrieves the chat agent's state for the given thread ID.
    """
    config = {"configurable": {"thread_id": thread_id}}
    state = await graph.aget_state(config)
    return state
