from langchain_core.messages import SystemMessage, HumanMessage
from app.services.llm_service import get_llm
from app.core.logging import logger
import yaml
from pathlib import Path

class PromptService:
    def __init__(self):
        self.llm = get_llm()
        
        # Load prompt from YAML
        prompt_path = Path(__file__).parent.parent / "prompts" / "prompt_image_generation.yaml"
        try:
            with open(prompt_path, "r") as f:
                prompt_data = yaml.safe_load(f)
                self.system_prompt = prompt_data.get("template_text", "")
                if not self.system_prompt:
                    logger.warning("Loaded system prompt template is empty.")
                    self.system_prompt = "You are an expert illustrator."
        except Exception as e:
            logger.error(f"Error loading system prompt from {prompt_path}: {e}")
            self.system_prompt = "You are an AI assistant."

    async def generate_optimized_prompt(
        self, 
        song_title: str, 
        song_text: str, 
        style: str, 
        image_count: int = 4, 
        feedback: str = None, 
        scene_index: int = None, 
        current_prompts: list[dict] = None
    ) -> str:
        """
        Uses LLM to optimize the user's input into a better prompt.
        Supports iterative refinement with feedback and history.
        """
        try:
            if feedback:
                history_context = ""
                if current_prompts:
                    history_context = f"CURRENT PROMPTS:\n{current_prompts}\n\n"
                
                refinement_instruction = f"USER FEEDBACK: {feedback}\n"
                if scene_index is not None:
                    refinement_instruction += f"ACTION: Please specifically refine Scene {scene_index + 1} based on this feedback, while ensuring it still fits the overall sequence.\n"
                else:
                    refinement_instruction += "ACTION: Please refine all scenes based on this feedback.\n"

                human_content = (
                    f"Refine the image prompts for:\n"
                    f"SONG TITLE: {song_title}\n"
                    f"SONG TEXT/LYRICS:\n{song_text}\n"
                    f"DESIRED STYLE: {style}\n\n"
                    f"{history_context}"
                    f"{refinement_instruction}"
                    f"IMPORTANT: Return the FULL JSON with all scenes updated as needed."
                )
            else:
                human_content = (
                    f"Please generate the image prompts based on this storage/song data:\n\n"
                    f"SONG TITLE: {song_title}\n"
                    f"SONG TEXT/LYRICS:\n{song_text}\n\n"
                    f"DESIRED STYLE: {style}\n"
                    f"NUMBER OF SCENES: {image_count}"
                )

            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=human_content)
            ]
            response = await self.llm.ainvoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error generating optimized prompt: {e}", exc_info=True)
            return song_text

def get_prompt_service():
    return PromptService()
