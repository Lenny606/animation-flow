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

    async def generate_optimized_prompt(self, song_title: str, song_text: str, style: str, image_count: int = 4) -> str:
        """
        Uses LLM to optimize the user's input into a better prompt.
        """
        try:
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=(
                    f"Please generate the image prompts based on this storage/song data:\n\n"
                    f"SONG TITLE: {song_title}\n"
                    f"SONG TEXT/LYRICS:\n{song_text}\n\n"
                    f"DESIRED STYLE: {style}\n"
                    f"NUMBER OF SCENES: {image_count}"
                ))
            ]
            # print(messages)
            response = await self.llm.ainvoke(messages)
            # print(response)
            return response.content
        except Exception as e:
            logger.error(f"Error generating optimized prompt: {e}", exc_info=True)
            # Fallback to original text if AI fails
            return song_text

def get_prompt_service():
    return PromptService()
