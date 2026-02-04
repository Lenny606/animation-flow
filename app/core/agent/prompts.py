from typing import Optional
from app.models.prompt_template import CustomPrompt
# Assuming a DB dependency or direct DB access will be injected/used.
# For simplicity in this step, we'll setup the basics and include a default fallback.

# Default Templates
DEFAULT_STORY_OUTLINE_TEMPLATE = """
You are a creative screenwriter.
Create a detailed story outline based on the following topic: "{topic}".
Style: {style}
Target Audience: {target_audience}

The outline should be structured as a sequence of events suitable for a {duration} second video.
Return just the story text.
"""

DEFAULT_SCENE_SCRIPTING_TEMPLATE = """
You are an expert visual director and scriptwriter.
Transform the following story outline into a structured list of scenes.

Story Outline:
{story_outline}

For each scene, provide:
1. Visual Description: A detailed prompt for an image generation model (like Midjourney). Be descriptive about lighting, composition, and style.
2. Voiceover: The script for the narrator.
3. Character Action: What is happening in the scene.
4. Estimated Duration: In seconds.

The output must be valid JSON matching the following structure:
[
  {
    "id": 1,
    "visual_description": "...",
    "voiceover": "...",
    "character_action": "...",
    "estimated_duration": 5
  }
]
"""

class PromptService:
    @staticmethod
    async def get_template(name: str, default: str) -> str:
        """
        Retrieves a prompt template. 
        In a real scenario, this would check the DB (Redis/MongoDB) for a custom override.
        For now, returns the default.
        """
        # TODO: Implement DB lookup for CustomPrompt with 'name'
        # e.g. prompt = await db.prompts.find_one({"name": name})
        # if prompt: return prompt.template_text
        
        return default

    @staticmethod
    async def get_story_outline_template() -> str:
        return await PromptService.get_template("story_outline", DEFAULT_STORY_OUTLINE_TEMPLATE)

    @staticmethod
    async def get_scene_scripting_template() -> str:
        return await PromptService.get_template("scene_scripting", DEFAULT_SCENE_SCRIPTING_TEMPLATE)
