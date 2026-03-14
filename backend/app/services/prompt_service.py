from langchain_core.prompts import ChatPromptTemplate
from app.services.llm_service import get_llm
from app.core.logging import logger

class PromptService:
    def __init__(self):
        self.llm = get_llm()
        self.system_prompt = (
            "You are an expert AI prompt engineer for animations and video generation. "
            "Your goal is to optimize or generate a highly descriptive and effective prompt "
            "for AI video models based on the user's input."
        )

    async def generate_optimized_prompt(self, user_input: str) -> str:
        """
        Uses LLM to optimize the user's input into a better prompt.
        """
        try:
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("user", "Optimize this prompt for an AI video model: {user_input}")
            ])
            
            chain = prompt_template | self.llm
            response = await chain.ainvoke({"user_input": user_input})
            
            return response.content
        except Exception as e:
            logger.error(f"Error generating optimized prompt: {e}")
            # Fallback to original text if AI fails
            return user_input

def get_prompt_service():
    return PromptService()
