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

# Standardize origins and add common variations
allowed_origins = settings.cors_origins_list
if "https://animation-flow-lac.vercel.app" not in allowed_origins:
    allowed_origins.append("https://animation-flow-lac.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*-lac\.vercel\.app|https://animation-flow-lac\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Accept", "X-Requested-With"],
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
