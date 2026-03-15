from app.core.config import get_settings
settings = get_settings()
print(f"ENVIRONMENT: '{settings.ENVIRONMENT}'")
print(f"BACKEND_URL: '{settings.BACKEND_URL}'")
print(f"IMAGE_PROVIDER: '{settings.IMAGE_PROVIDER}'")
print(f"OPENAI_API_KEY set: {bool(settings.OPENAI_API_KEY)}")
