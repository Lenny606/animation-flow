from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.core.llm_factory import LLMFactory
from app.core.config import get_settings

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

async def call_model(state: AgentState):
    """
    Calls the LLM with the current state's messages and returns the AI's response.
    """
    settings = get_settings()
    llm_factory = LLMFactory(settings=settings)
    llm = llm_factory.create_llm()
    
    messages = state['messages']
    response = await llm.ainvoke(messages)
    return {"messages": [response]}

def create_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("agent", call_model)
    
    workflow.set_entry_point("agent")
    
    workflow.add_edge("agent", END)
    
    checkpointer = MemorySaver()
    return workflow.compile(checkpointer=checkpointer)

graph = create_graph()
