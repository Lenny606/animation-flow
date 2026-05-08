from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Orchestration App"
    VERSION: str = "0.1.0"
    API_V1_STR: str = ""
    LOG_FILE_PATH: str = "/app/logs/app.log"
    ERROR_LOG_FILE_PATH: str = "/app/logs/error.log"
    ENVIRONMENT: str = "development" # development, production
    DISABLE_AUTH: bool = False

    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "ai_app_db"
    
    REDIS_URL: str = "redis://localhost:6379/0"

    SECRET_KEY: str = "changethiskeyinproduction"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Cookie Settings
    AUTH_COOKIE_NAME: str = "access_token"
    COOKIE_SECURE: bool = True 
    COOKIE_SAMESITE: str = "none"

    BACKEND_URL: str = "https://animation-flow-r25n.vercel.app"
    FRONTEND_URL: str = "https://animation-flow-r25n.vercel.app"
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5172,http://127.0.0.1:5172,http://localhost:3000,http://127.0.0.1:3000,https://animation-flow-lac.vercel.app,https://animation-flow-1pys.vercel.app,https://animation-flow-r25n.vercel.app"
    
    # LangSmith Settings
    LANGCHAIN_TRACING_V2: str = "false"
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "animation-flow"

    # LLM Settings
    OPENAI_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL_IMAGEN_KEY: str = ""
    OPENAI_MODEL_NAME: str = "gpt-3.5-turbo"
    GEMINI_MODEL_NAME: str = "gemini-2.5-flash"
    IMAGEN_MODEL_NAME: str = "gemini-2.5-flash-image"
    OPENAI_IMAGE_MODEL_NAME: str = "dall-e-3"
    IMAGE_PROVIDER: str = "openai"
    LOCAL_LLM_BASE_URL: str = "http://localhost:11434/v1"
    LOCAL_LLM_API_KEY: str = "lm-studio"
    LOCAL_LLM_MODEL_NAME: str = "llama2"

    LLM_RETRY_MAX_ATTEMPTS: int = 3
    LLM_FALLBACK_ENABLED: bool = True

    @property
    def cors_origins_list(self) -> list[str]:
        if not self.CORS_ORIGINS:
            return []
        # Strip potential quotes and split
        raw_origins = self.CORS_ORIGINS.strip('"').strip("'").strip()
        return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()
