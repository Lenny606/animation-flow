import asyncio
from typing import TypedDict, List, Optional
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

from app.core.llm_factory import LLMFactory
from app.interfaces.image_provider import ImageProviderFactory
from app.models.scenario import Scenario
from app.models.asset import ImageAsset

# --- Internal Models for the Agent ---
class VisualFrameRequest(BaseModel):
    order: int
    visual_description: str = Field(..., description="Optimized prompt for DALL-E")
    vo_context: Optional[str] = Field(None, description="Context from voiceover")

class ImageAgentState(TypedDict):
    scenario: dict # Input Scenario
    planned_frames: Optional[List[dict]] # Output of Visual Planner
    generated_assets: Optional[List[dict]] # Final Assets
    provider: str

# --- Nodes ---

async def visual_planner_node(state: ImageAgentState):
    """
    LLM analyzes the scenario and decides on 10-15 keyframes.
    """
    scenario_data = state["scenario"]
    provider = state.get("provider", "openai") # LLM provider for planning
    llm = LLMFactory.create_llm(provider=provider, temperature=0.7)
    
    # Construct context from scenario
    scenes_text = ""
    for scene in scenario_data.get("scenes", []):
        scenes_text += f"Scene {scene.get('id')}: {scene.get('visual_description')} (VO: {scene.get('voiceover')})\n"
        
    prompt = f"""
    You are an expert Storyboard Artist.
    Your task is to review the following video script and plan the visual assets needed.
    
    Constraints:
    1.  The video needs between 10 and 15 unique images (keyframes) to maintain visual interest.
    2.  You can combine short scenes into one image, or split long scenes into multiple images.
    3.  For each keyframe, write a highly detailed, optimized prompt for DALL-E 3. 
        - Include style keywords: "{scenario_data.get('style')}"
        - Ensure visual consistency (mention character details repeatedly).
    
    Script:
    {scenes_text}
    
    Output strictly a JSON list of objects with keys: "order" (int), "visual_description" (str).
    """
    
    parser = JsonOutputParser(pydantic_object=List[VisualFrameRequest])
    
    response = await llm.ainvoke([
        SystemMessage(content="You are a JSON-speaking Storyboard API."),
        HumanMessage(content=prompt)
    ])
    
    try:
        planned_frames = parser.parse(response.content)
    except:
        import json
        # naive fallback
        clean_content = response.content.replace("```json", "").replace("```", "")
        planned_frames = json.loads(clean_content)
        
    return {"planned_frames": planned_frames}

async def image_generation_node(state: ImageAgentState):
    """
    Execution node: Calls the Image Provider for each planned frame.
    """
    frames = state["planned_frames"]
    scenario_id = state["scenario"].get("_id", "temp_id")
    
    # We use the factory (defaulting to openai for images for now)
    image_provider = ImageProviderFactory.get_provider("openai")
    
    assets = []
    
    # We can run these in parallel or sequence. 
    # Parallel is faster but hits rate limits. 
    # Let's do a semaphore-limited parallel approach or simple sequential for safety.
    
    # Sequential for MVP stability
    for frame in frames:
        try:
            print(f"Generating image {frame['order']}...")
            result = await image_provider.generate_image(prompt=frame['visual_description'])
            
            asset = ImageAsset(
                scenario_id=scenario_id,
                prompt_used=frame['visual_description'],
                image_url=result.url,
                order=frame['order'],
                provider=result.provider
            )
            assets.append(asset.model_dump())
        except Exception as e:
            print(f"Failed to generate image {frame['order']}: {e}")
            
    return {"generated_assets": assets}

# --- Graph Definition ---
workflow = StateGraph(ImageAgentState)

workflow.add_node("visual_planner", visual_planner_node)
workflow.add_node("image_generator", image_generation_node)

workflow.set_entry_point("visual_planner")
workflow.add_edge("visual_planner", "image_generator")
workflow.add_edge("image_generator", END)

image_agent = workflow.compile()
