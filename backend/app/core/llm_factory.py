import os
from typing import Optional, Literal
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel

class LLMFactory:
    @staticmethod
    def create_llm(
        provider: Literal["openai", "gemini", "local"] = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.7
    ) -> BaseChatModel:
        """
        Factory method to create a LangChain Chat Model based on the provider.
        """
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is not set")
            # Default to gpt-3.5-turbo if not specified, or allow env override
            final_model = model_name or os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
            return ChatOpenAI(
                model=final_model,
                temperature=temperature,
                api_key=api_key
            )
            
        elif provider == "gemini":
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable is not set")
            final_model = model_name or os.getenv("GEMINI_MODEL_NAME", "gemini-pro")
            return ChatGoogleGenerativeAI(
                model=final_model,
                temperature=temperature,
                google_api_key=api_key
            )
            
        elif provider == "local":
            # Assuming local models utilize an OpenAI-compatible API (e.g., Ollama, vLLM)
            base_url = os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:11434/v1")
            api_key = os.getenv("LOCAL_LLM_API_KEY", "lm-studio") # dummy key often needed
            final_model = model_name or os.getenv("LOCAL_LLM_MODEL_NAME", "llama2")
            return ChatOpenAI(
                base_url=base_url,
                api_key=api_key,
                model=final_model,
                temperature=temperature
            )

        raise ValueError(f"Unsupported LLM provider: {provider}")
