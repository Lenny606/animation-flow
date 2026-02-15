from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.logging import logger

async def http_error_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error occurred: {exc.detail} - Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error occurred: {exc} - Path: {request.url.path}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
