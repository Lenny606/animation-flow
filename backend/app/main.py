from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.config import get_settings

from app.core.error_handling import http_error_handler, global_exception_handler
from fastapi.exceptions import HTTPException
from app.db.mongodb import db, MongoDB
from app.db.redis import redis_client
from app.routers import auth, agent, scenarios, assets, video, jenko
from app.core.logging import logger
from contextlib import asynccontextmanager

settings = get_settings()

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

origins = [
    "https://animation-flow-lac.vercel.app",
    "https://animation-flow-1pys.vercel.app",
    "http://localhost:5173",
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

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

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(agent.router, prefix="/agent", tags=["agent"])
app.include_router(scenarios.router)
app.include_router(assets.router)
app.include_router(video.router)
app.include_router(jenko.router)

@app.get("/")
async def root():
    return {"message": "Welcome to AI Orchestration API"}


