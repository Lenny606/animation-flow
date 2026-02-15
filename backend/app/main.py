from fastapi import FastAPI
from app.core.config import get_settings

from app.core.error_handling import http_error_handler, global_exception_handler
from fastapi.exceptions import HTTPException
from app.db.mongodb import db, MongoDB
from app.db.redis import redis_client
from app.routers import auth, agent, scenarios, assets, video
from contextlib import asynccontextmanager

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db.connect()
    await redis_client.connect()
    yield
    # Shutdown
    db.close()
    await redis_client.close()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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

@app.get("/")
async def root():
    return {"message": "Welcome to AI Orchestration API"}
