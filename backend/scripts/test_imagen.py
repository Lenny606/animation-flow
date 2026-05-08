import asyncio
import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from app.services.image_service import get_image_service
from app.core.config import get_settings

async def test_imagen():
    settings = get_settings()
    # Ensure GEMINI_API_KEY is set in environment or settings
    if not settings.GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not set in settings.")
        return

    print(f"Testing Gemini Imagen with model: {settings.IMAGEN_MODEL_NAME}")
    
    image_service = get_image_service()
    prompt = "A futuristic cyberpunk city with neon lights and flying cars, high resolution, digital art style"
    
    try:
        print(f"Generating image for prompt: {prompt}")
        image_url = await image_service.generate_single_image(prompt)
        print(f"Success! Image URL: {image_url}")
        
        if "placehold.co" in image_url:
            print("Warning: Received a placeholder URL. Check logs for errors.")
        else:
            print("Successfully received a generated image URL.")
            
    except Exception as e:
        print(f"An error occurred during testing: {e}")

if __name__ == "__main__":
    asyncio.run(test_imagen())
