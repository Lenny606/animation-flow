from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()

def get_llm():
    """
    Initialize and return the Google Gemini LLM.
    """
    api_key = settings.GEMINI_API_KEY or settings.GOOGLE_API_KEY
    
    if not api_key:
        logger.warning("Neither GEMINI_API_KEY nor GOOGLE_API_KEY is set. Gemini LLM may not function correctly.")
    
    return ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL_NAME,
        google_api_key=api_key,
        temperature=0.7,
    )
