from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Orchestration App"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "ai_app_db"
    
    REDIS_URL: str = "redis://localhost:6379/0"

    SECRET_KEY: str = "changethiskeyinproduction"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:5173"
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000,https://animation-flow-lac.vercel.app"

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
