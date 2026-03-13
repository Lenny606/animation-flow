from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

# 1. Define the State
class AgentState(TypedDict):
    # 'messages' is a list of BaseMessage, and we provide an 'add' reducer which LangGraph uses to update the list
    messages: Annotated[list[BaseMessage], lambda x, y: x + y]
    next_node: str

# 2. Define Nodes
def call_model(state: AgentState):
    """Call the LLM and return the updated state."""
    # Example: model = ChatOpenAI()
    # response = model.invoke(state['messages'])
    # return {"messages": [response]}
    print("--- CALLING MODEL ---")
    return {"messages": []}

def decision_node(state: AgentState):
    """Decide where to go next based on the state."""
    # Logic to return where to go next
    if state.get("next_node") == "end":
        return "end"
    return "continue"

# 3. Create the Graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", call_model)

# Set entry point
workflow.add_edge(START, "agent")

# Set conditional or direct edges
workflow.add_edge("agent", END)

# 4. Compile the Graph
app = workflow.compile()

# Optional: Run the graph
# inputs = {"messages": [("user", "Hello graph!")]}
# for output in app.stream(inputs):
#     print(output)
