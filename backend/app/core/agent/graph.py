from typing import TypedDict, List, Optional
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.core.llm_factory import LLMFactory, get_llm_factory
from app.core.agent.prompts import PromptService, get_prompt_service
from app.core.config import get_settings
from app.db.mongodb import get_database
from app.models.scenario import Scene, Scenario

# Define Agent State
class AgentState(TypedDict):
    # Inputs
    topic: str
    style: str
    target_audience: str
    duration: int
    llm_provider: str
    
    # Internal/Outputs
    story_outline: Optional[str]
    scenes_data: Optional[List[dict]]
    final_scenario: Optional[dict]

# Node: Story Generator
async def generate_story(state: AgentState):
    provider = state.get("llm_provider", "openai")
    
    settings = get_settings()
    llm_factory = get_llm_factory(settings)
    llm = llm_factory.create_llm(provider=provider, temperature=0.7)
    
    db = await get_database()
    prompt_service = await get_prompt_service(db)
    template = await prompt_service.get_story_outline_template()
    prompt = template.format(
        topic=state["topic"],
        style=state["style"],
        target_audience=state["target_audience"],
        duration=state.get("duration", 60) # Default 60s if missing
    )
    
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return {"story_outline": response.content}

# Node: Scene Scripting
async def script_scenes(state: AgentState):
    provider = state.get("llm_provider", "openai")
    # Use json mode if supported, or rely on parsing
    settings = get_settings()
    llm_factory = get_llm_factory(settings)
    llm = llm_factory.create_llm(provider=provider, temperature=0.7)
    
    db = await get_database()
    prompt_service = await get_prompt_service(db)
    template = await prompt_service.get_scene_scripting_template()
    prompt = template.format(story_outline=state["story_outline"])
    
    # We can use PydanticOutputParser or JsonOutputParser
    parser = JsonOutputParser(pydantic_object=List[Scene])
    
    response = await llm.ainvoke([
        SystemMessage(content="You are a JSON-speaking API. Output strictly JSON."),
        HumanMessage(content=prompt)
    ])
    
    try:
        parsed_scenes = parser.parse(response.content)
    except Exception:
        # Fallback or retry logic could go here. 
        # For now, simplistic parsing attempt
        import json
        parsed_scenes = json.loads(response.content.replace("```json", "").replace("```", ""))

    return {"scenes_data": parsed_scenes}

# Node: Final/Aggregation (Optional, but good for cleanup)
async def finalize_scenario(state: AgentState):
    # Construct the final Scenario object structure
    scenario_data = {
        "title": f"Scenario: {state['topic']}",
        "topic": state["topic"],
        "style": state["style"],
        "target_audience": state["target_audience"],
        "scenes": state["scenes_data"],
        "llm_provider": state.get("llm_provider", "openai")
    }
    return {"final_scenario": scenario_data}

# Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("story_generator", generate_story)
workflow.add_node("scene_scripting", script_scenes)
workflow.add_node("finalize", finalize_scenario)

workflow.set_entry_point("story_generator")

workflow.add_edge("story_generator", "scene_scripting")
workflow.add_edge("scene_scripting", "finalize")
workflow.add_edge("finalize", END)

# Compile the app
checkpointer = MemorySaver()
scenario_agent = workflow.compile(checkpointer=checkpointer)
