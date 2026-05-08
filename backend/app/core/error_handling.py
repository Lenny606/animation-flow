from typing import Any, Dict, Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.logging import logger

class BaseAPIException(Exception):
    """Base class for all custom API exceptions."""
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "Internal Server Error",
        headers: Optional[Dict[str, str]] = None,
        extra: Optional[Dict[str, Any]] = None
    ):
        self.status_code = status_code
        self.detail = detail
        self.headers = headers
        self.extra = extra
        super().__init__(detail)

class NotFoundException(BaseAPIException):
    def __init__(self, detail: str = "Resource not found", extra: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, extra=extra)

class BadRequestException(BaseAPIException):
    def __init__(self, detail: str = "Bad request", extra: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, extra=extra)

class UnauthorizedException(BaseAPIException):
    def __init__(self, detail: str = "Unauthorized", extra: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
            extra=extra
        )

class ForbiddenException(BaseAPIException):
    def __init__(self, detail: str = "Forbidden", extra: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail, extra=extra)

class ConflictException(BaseAPIException):
    def __init__(self, detail: str = "Conflict", extra: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail, extra=extra)

class InternalServerException(BaseAPIException):
    def __init__(self, detail: str = "Internal server error", extra: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail, extra=extra)

async def api_exception_handler(request: Request, exc: BaseAPIException):
    logger.error(f"API Error: {exc.detail} - Path: {request.url.path} - Code: {exc.status_code}")
    content = {"detail": exc.detail}
    if exc.extra:
        content["extra"] = exc.extra
    
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
        headers=exc.headers,
    )

async def http_error_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error occurred: {exc.detail} - Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error occurred: {exc.errors()} - Path: {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
        },
    )

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error occurred: {exc} - Path: {request.url.path}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected internal server error occurred",
        },
    )
