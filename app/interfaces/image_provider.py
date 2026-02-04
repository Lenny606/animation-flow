from abc import ABC, abstractmethod
from typing import List, Optional
import os
import aiohttp
import base64
from datetime import datetime

class ImageGenerationResult:
    def __init__(self, url: str, provider: str, local_path: Optional[str] = None):
        self.url = url
        self.provider = provider
        self.local_path = local_path

class BaseImageProvider(ABC):
    @abstractmethod
    async def generate_image(self, prompt: str, size: str = "1024x1024") -> ImageGenerationResult:
        pass

class OpenAIImageProvider(BaseImageProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.output_dir = "static/images"
        os.makedirs(self.output_dir, exist_ok=True)

    async def generate_image(self, prompt: str, size: str = "1024x1024") -> ImageGenerationResult:
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": size,
            "response_format": "b64_json" # Use b64 to save locally reliably
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"OpenAI Image Gen Error: {error_text}")
                
                data = await response.json()
                b64_data = data["data"][0]["b64_json"]
                
                # Save locally
                timestamp = int(datetime.now().timestamp())
                filename = f"img_{timestamp}_{os.urandom(4).hex()}.png"
                local_path = os.path.join(self.output_dir, filename)
                
                with open(local_path, "wb") as f:
                    f.write(base64.b64decode(b64_data))
                
                return ImageGenerationResult(
                    url=local_path, # serving path 
                    provider="openai-dalle-3",
                    local_path=local_path
                )

class ImageProviderFactory:
    @staticmethod
    def get_provider(provider_name: str = "openai") -> BaseImageProvider:
        if provider_name == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set")
            return OpenAIImageProvider(api_key)
        
        raise ValueError(f"Unknown provider: {provider_name}")
