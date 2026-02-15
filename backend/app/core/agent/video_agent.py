import asyncio
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END

from app.interfaces.video_provider import VideoProviderFactory
from app.models.asset import ImageAsset, VideoAsset
from app.models.scenario import Scenario

class VideoAgentState(TypedDict):
    scenario_id: str
    image_assets: List[dict] # Input Image Assets
    video_assets: Optional[List[dict]] # Output Video Assets
    generate_voiceover: bool # Conditional Flag
    provider: str

# --- Nodes ---

async def video_generation_node(state: VideoAgentState):
    """
    Iterates through image assets and generates video clips.
    """
    images = state["image_assets"]
    provider_name = state.get("provider", "mock")
    scenario_id = state["scenario_id"]
    
    video_provider = VideoProviderFactory.get_provider(provider_name)
    generated_videos = []
    
    for img_data in images:
        try:
            # We assume img_data matches ImageAsset structure
            image_url = img_data.get("image_url")
            prompt = img_data.get("prompt_used", "Animate this scene")
            
            # Call provider
            job = await video_provider.generate_video(image_url, prompt)
            
            if job.status == "completed":
                video_asset = VideoAsset(
                    scenario_id=scenario_id,
                    image_asset_id=img_data.get("id") or img_data.get("_id") or "unknown",
                    video_url=job.video_url,
                    provider=provider_name,
                    status="completed"
                )
                generated_videos.append(video_asset.model_dump())
            else:
                # Handle async jobs (pending) - for MVP we assume completed or just mark pending
                pass
                
        except Exception as e:
            print(f"Video gen failed for {img_data.get('id')}: {str(e)}")
            
    return {"video_assets": generated_videos}

async def voiceover_node(state: VideoAgentState):
    """
    Dummy VO node.
    """
    print("Generating Voiceover (DUMMY)...")
    return {}

# --- Conditional Logic ---

def should_generate_voiceover(state: VideoAgentState):
    if state.get("generate_voiceover", False):
        return "voiceover_node"
    return END

# --- Graph Definition ---
workflow = StateGraph(VideoAgentState)

workflow.add_node("video_generation", video_generation_node)
workflow.add_node("voiceover_node", voiceover_node)

workflow.set_entry_point("video_generation")

workflow.add_conditional_edges(
    "video_generation",
    should_generate_voiceover
)

workflow.add_edge("voiceover_node", END)

video_agent = workflow.compile()
