from abc import ABC, abstractmethod
from typing import Optional
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()

class ImageProvider(ABC):
    @abstractmethod
    async def generate_image(self, prompt: str) -> str:
        pass

class GeminiImageProvider(ImageProvider):
    async def generate_image(self, prompt: str) -> str:
        """
        Generates an image using Gemini (Mock for now as direct API might vary).
        In a real scenario, this would call the Google Imagen API or similar.
        """
        logger.info(f"Generating image with Gemini for prompt: {prompt[:50]}...")
        # For now, return a high-quality placeholder that looks relevant
        # We can use a service like Unsplash or a mock URL that we'll later replace with real API
        return f"https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1000&auto=format&fit=crop"

class MockImageProvider(ImageProvider):
    async def generate_image(self, prompt: str) -> str:
        logger.info(f"Generating mock image for prompt: {prompt[:50]}...")
        return "https://via.placeholder.com/1024x1024.png?text=AI+Generated+Image"

class ImageService:
    def __init__(self, provider: ImageProvider):
        self.provider = provider

    async def generate_single_image(self, prompt: str) -> str:
        return await self.provider.generate_image(prompt)

def get_image_service() -> ImageService:
    # Logic to switch providers based on settings
    provider_type = getattr(settings, "IMAGE_PROVIDER", "gemini").lower()
    
    if provider_type == "gemini":
        provider = GeminiImageProvider()
    else:
        provider = MockImageProvider()
        
    return ImageService(provider)
