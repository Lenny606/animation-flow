import asyncio
import os
import sys
from pathlib import Path

# Add the backend directory to sys.path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from app.services.utils_service import get_utils_service

async def test_fetch_image():
    service = get_utils_service()
    url = "https://placehold.co/1024x1024/ef4444/white?text=Test+Download"
    filename = "test_image.png"
    
    print(f"Attempting to download image from {url}...")
    try:
        relative_path = await service.fetch_image_by_url(url, filename)
        print(f"Success! Image saved to: {relative_path}")
        
        # Verify file existence
        full_path = backend_dir / relative_path.lstrip('/')
        if full_path.exists():
            print(f"Verified: File exists at {full_path}")
            print(f"File size: {full_path.stat().st_size} bytes")
        else:
            print(f"Error: File does not exist at {full_path}")
            
    except Exception as e:
        print(f"Failed to fetch image: {e}")

if __name__ == "__main__":
    asyncio.run(test_fetch_image())
