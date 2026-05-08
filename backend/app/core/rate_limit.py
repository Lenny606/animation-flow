from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request
from jose import jwt, JWTError
from typing import Callable, Optional
from app.core.config import get_settings
from app.models.user import UserRole

settings = get_settings()

def user_id_key_func(request: Request) -> str:
    """
    Key function for slowapi that uses user ID from JWT if available,
    otherwise falls back to remote address.
    """
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if email:
                return email
        except (JWTError, AttributeError):
            pass
    
    return get_remote_address(request)

limiter = Limiter(key_func=user_id_key_func)

def get_role_limit(
    free_limit: str, 
    pro_limit: str, 
    admin_limit: Optional[str] = None
) -> Callable[[Request], str]:
    """
    Returns a dynamic limit string based on the user's role.
    """
    def dynamic_limit(request: Request) -> str:
        auth_header = request.headers.get("Authorization")
        role = UserRole.FREE
        
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                role = payload.get("role", UserRole.FREE)
            except (JWTError, AttributeError):
                pass

        if role == UserRole.ADMIN:
            return admin_limit or pro_limit
        if role == UserRole.PRO:
            return pro_limit
        return free_limit
        
    return dynamic_limit
