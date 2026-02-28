from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.config import get_settings
import os

from app.core.error_handling import (
    http_error_handler, 
    global_exception_handler, 
    api_exception_handler,
    validation_exception_handler,
    BaseAPIException
)
from fastapi.exceptions import HTTPException, RequestValidationError
from app.db.mongodb import db, MongoDB
from app.db.redis import redis_client
from app.routers import auth, agent, scenarios, assets, video, jenko, songs
from app.core.logging import logger
from app.core.rate_limit import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

settings = get_settings()

# Initialize LangSmith environment variables
os.environ["LANGCHAIN_TRACING_V2"] = settings.LANGCHAIN_TRACING_V2
os.environ["LANGCHAIN_ENDPOINT"] = settings.LANGCHAIN_ENDPOINT
os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT

from app.core.agent.prompts import PromptService, get_prompt_service
from app.db.mongodb import get_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        db.connect()
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB during startup: {e}")
    
    try:
        await redis_client.connect()
    except Exception as e:
        logger.error(f"Failed to connect to Redis during startup: {e}")

    # Sanity check for prompts
    try:
        database = await get_database()
        prompt_service = await get_prompt_service(database)
        story_prompt = await prompt_service.get_story_outline_template()
        if story_prompt:
            logger.info("Prompts initialized and loaded successfully.")
        else:
            logger.warning("No prompt templates found during startup.")
    except Exception as e:
        logger.error(f"Error checking prompts on startup: {e}")
    
    yield
    # Shutdown
    db.close()
    await redis_client.close()

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
AI Orchestration API powers the Animation Flow application, providing endpoints for:
* **Authentication**: User registration and login.
* **AI Agent**: Natural language interaction with the system.
* **Scenarios**: Generating and managing video scripts.
* **Assets**: Generating image assets for scenes.
* **Video**: Planning and executing video generation.
* **Jenko**: Specialized image metadata management.
* **Songs**: Managing a library of songs.
""",
    lifespan=lifespan,
    contact={
        "name": "API Support",
        "url": "https://github.com/tomas-p/animation-flow",
    },
    license_info={
        "name": "MIT",
    },
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Standard CORSMiddleware as the primary handler
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(BaseAPIException, api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(agent.router, prefix=f"{settings.API_V1_STR}/agent", tags=["AI Agent"])
app.include_router(scenarios.router, prefix=f"{settings.API_V1_STR}/scenarios", tags=["Scenarios"])
app.include_router(assets.router, prefix=f"{settings.API_V1_STR}/assets", tags=["Assets"])
app.include_router(video.router, prefix=f"{settings.API_V1_STR}/video", tags=["Video"])
app.include_router(jenko.router, prefix=f"{settings.API_V1_STR}/jenko", tags=["Jenko"])
app.include_router(songs.router, prefix=f"{settings.API_V1_STR}/songs", tags=["Songs"])

@app.get("/")
async def root():
    return {"message": "Welcome to AI Orchestration API"}


