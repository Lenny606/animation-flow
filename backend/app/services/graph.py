from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

def call_model(state: AgentState):
    # In a real app, you would call an LLM here.
    # For skeleton purposes, we simulate a response.
    messages = state['messages']
    last_message = messages[-1]
    response = f"Echo: {last_message.content}"
    return {"messages": [AIMessage(content=response)]}

def create_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("agent", call_model)
    
    workflow.set_entry_point("agent")
    
    workflow.add_edge("agent", END)
    
    return workflow.compile()

graph = create_graph()
