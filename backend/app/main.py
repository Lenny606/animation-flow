from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.config import get_settings

from app.core.error_handling import http_error_handler, global_exception_handler
from fastapi.exceptions import HTTPException
from app.db.mongodb import db, MongoDB
from app.db.redis import redis_client
from app.routers import auth, agent, scenarios, assets, video, jenko, songs
from app.core.logging import logger
from app.core.rate_limit import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

settings = get_settings()

from app.core.agent.prompts import PromptService

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
        story_prompt = await PromptService.get_story_outline_template()
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

origins = [
    "https://animation-flow-lac.vercel.app",
    "https://animation-flow-1pys.vercel.app",
    "http://localhost:5173",
]

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

@app.middleware("http")
async def cors_handler(request: Request, call_next):
    origin = request.headers.get("origin")
    allow_origin = origin if origin in origins else origins[0]
    
    # Handle preflight OPTIONS requests manually as a fallback
    if request.method == "OPTIONS":
        return JSONResponse(
            content="OK",
            headers={
                "Access-Control-Allow-Origin": allow_origin,
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Credentials": "true",
            },
        )
    
    response = await call_next(request)
    
    # Add headers to all responses if not present
    if "Access-Control-Allow-Origin" not in response.headers:
        response.headers["Access-Control-Allow-Origin"] = allow_origin
    response.headers["Access-Control-Allow-Credentials"] = "true"
    
    return response

# Standard CORSMiddleware as the primary handler
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(agent.router, prefix="/agent", tags=["AI Agent"])
app.include_router(scenarios.router, tags=["Scenarios"])
app.include_router(assets.router, tags=["Assets"])
app.include_router(video.router, tags=["Video"])
app.include_router(jenko.router, tags=["Jenko"])
app.include_router(songs.router, tags=["Songs"])

@app.get("/")
async def root():
    return {"message": "Welcome to AI Orchestration API"}


