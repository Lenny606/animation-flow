import os
from typing import Optional, Literal, List
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel
from app.core.config import get_settings

class LLMFactory:
    @staticmethod
    def create_llm(
        provider: Literal["openai", "gemini", "local"] = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        with_retry: bool = True,
        with_fallback: bool = True
    ) -> BaseChatModel:
        """
        Factory method to create a LangChain Chat Model with optional retry and fallback logic.
        """
        settings = get_settings()
        
        # 1. Create the primary LLM
        primary_llm = LLMFactory._create_base_llm(provider, model_name, temperature)
        
        # 2. Add Retry Logic
        if with_retry:
            primary_llm = primary_llm.with_retry(
                stop_after_attempt=settings.LLM_RETRY_MAX_ATTEMPTS
            )
            
        # 3. Add Fallback Logic
        if with_fallback and settings.LLM_FALLBACK_ENABLED:
            fallbacks = LLMFactory._get_fallbacks(provider, temperature)
            if fallbacks:
                primary_llm = primary_llm.with_fallbacks(fallbacks)
                
        return primary_llm

    @staticmethod
    def _create_base_llm(
        provider: str,
        model_name: Optional[str] = None,
        temperature: float = 0.7
    ) -> BaseChatModel:
        settings = get_settings()
        
        if provider == "openai":
            api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY is not set")
            final_model = model_name or settings.OPENAI_MODEL_NAME
            return ChatOpenAI(
                model=final_model,
                temperature=temperature,
                api_key=api_key
            )
            
        elif provider == "gemini":
            api_key = settings.GOOGLE_API_KEY or os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY is not set")
            final_model = model_name or settings.GEMINI_MODEL_NAME
            return ChatGoogleGenerativeAI(
                model=final_model,
                temperature=temperature,
                google_api_key=api_key
            )
            
        elif provider == "local":
            base_url = settings.LOCAL_LLM_BASE_URL
            api_key = settings.LOCAL_LLM_API_KEY
            final_model = model_name or settings.LOCAL_LLM_MODEL_NAME
            return ChatOpenAI(
                base_url=base_url,
                api_key=api_key,
                model=final_model,
                temperature=temperature
            )

        raise ValueError(f"Unsupported LLM provider: {provider}")

    @staticmethod
    def _get_fallbacks(current_provider: str, temperature: float) -> List[BaseChatModel]:
        """
        Returns a list of fallback models based on the current provider.
        """
        settings = get_settings()
        fallbacks = []
        
        # Define priority order for fallbacks
        providers_priority = ["openai", "gemini"]
        
        for provider in providers_priority:
            if provider == current_provider:
                continue
                
            try:
                # Check if API key exists for fallback provider
                if provider == "openai" and (settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")):
                    fallbacks.append(LLMFactory._create_base_llm("openai", temperature=temperature))
                elif provider == "gemini" and (settings.GOOGLE_API_KEY or os.getenv("GOOGLE_API_KEY")):
                    fallbacks.append(LLMFactory._create_base_llm("gemini", temperature=temperature))
            except Exception:
                # If we can't create a fallback, just skip it
                continue
                
        return fallbacks
