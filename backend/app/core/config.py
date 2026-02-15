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

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()
