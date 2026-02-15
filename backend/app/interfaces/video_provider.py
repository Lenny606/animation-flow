from abc import ABC, abstractmethod
from typing import Optional
import os
import asyncio
from datetime import datetime

class VideoJob:
    def __init__(self, job_id: str, status: str, video_url: Optional[str] = None):
        self.job_id = job_id
        self.status = status
        self.video_url = video_url

class BaseVideoProvider(ABC):
    @abstractmethod
    async def generate_video(self, image_url: str, prompt: str) -> VideoJob:
        pass

class MockVideoProvider(BaseVideoProvider):
    def __init__(self):
        self.output_dir = "static/videos"
        os.makedirs(self.output_dir, exist_ok=True)

    async def generate_video(self, image_url: str, prompt: str) -> VideoJob:
        # Simulate processing time
        await asyncio.sleep(2) 
        
        # Create a dummy video file
        timestamp = int(datetime.now().timestamp())
        filename = f"vid_{timestamp}_{os.urandom(4).hex()}.mp4"
        local_path = os.path.join(self.output_dir, filename)
        
        # Write dummy content
        with open(local_path, "wb") as f:
            f.write(b"mock video content")
            
        return VideoJob(
            job_id=f"mock_{timestamp}",
            status="completed",
            video_url=local_path
        )

# Placeholder for real providers like Runway or Luma
class RunwayVideoProvider(BaseVideoProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate_video(self, image_url: str, prompt: str) -> VideoJob:
        # TODO: Implement actual API call
        raise NotImplementedError("Runway provider not fully implemented yet.")

class VideoProviderFactory:
    @staticmethod
    def get_provider(provider_name: str = "mock") -> BaseVideoProvider:
        if provider_name == "mock":
            return MockVideoProvider()
        elif provider_name == "runway":
             api_key = os.getenv("RUNWAY_API_KEY") # Example
             return RunwayVideoProvider(api_key)
        
        return MockVideoProvider() # Default to mock
