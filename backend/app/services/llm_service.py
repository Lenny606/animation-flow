from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()

def get_llm():
    """
    Initialize and return the Google Gemini LLM.
    """
    if not settings.GOOGLE_API_KEY:
        logger.error("GOOGLE_API_KEY is not set.")
        raise ValueError("GOOGLE_API_KEY is not set. Gemini LLM cannot be initialized.")
    
    return ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL_NAME,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.7,
    )
