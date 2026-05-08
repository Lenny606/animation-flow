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
from app.routers import auth, scenarios, assets, video, jenko, songs, prompts
from app.core.logging import logger
from app.core.rate_limit import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from pathlib import Path

settings = get_settings()

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

# Ensure static directory exists
try:
    static_path = Path("static")
    static_path.mkdir(exist_ok=True)
    (static_path / "generated_images").mkdir(exist_ok=True, parents=True)
except (OSError, IOError) as e:
    logger.warning(f"Could not create static directory: {e}")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(BaseAPIException, api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(scenarios.router, prefix=f"{settings.API_V1_STR}/scenarios", tags=["Scenarios"])
app.include_router(assets.router, prefix=f"{settings.API_V1_STR}/assets", tags=["Assets"])
app.include_router(video.router, prefix=f"{settings.API_V1_STR}/video", tags=["Video"])
app.include_router(jenko.router, prefix=f"{settings.API_V1_STR}/jenko", tags=["Jenko"])
app.include_router(songs.router, prefix=f"{settings.API_V1_STR}/songs", tags=["Songs"])
app.include_router(prompts.router, prefix=f"{settings.API_V1_STR}/prompts", tags=["Prompts"])

@app.get("/")
async def root():
    return {"message": "Welcome to AI Orchestration API"}


