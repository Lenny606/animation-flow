import os
import httpx
from typing import Optional
from app.core.logging import logger
from app.core.config import get_settings
from pathlib import Path

settings = get_settings()

class UtilsService:
    def __init__(self):
        # Base directory for static files
        self.static_dir = Path("static")
        self.images_dir = self.static_dir / "images"
        
        # Ensure directories exist
        try:
            self.images_dir.mkdir(parents=True, exist_ok=True)
        except (OSError, IOError) as e:
            logger.warning(f"Could not create images directory: {e}")

    async def fetch_image_by_url(self, url: str, filename: Optional[str] = None) -> str:
        """
        Downloads an image from a URL and saves it to the backend's static folder.
        
        Args:
            url: The URL of the image to download.
            filename: Optional filename to save the image as. If not provided, 
                      it will be extracted from the URL or generated.
                      
        Returns:
            The local path or relative URL to the saved image.
        """
        try:
            if not filename:
                # Extract filename from URL or use a default
                url_path = Path(url.split('?')[0])
                filename = url_path.name
                if not filename or '.' not in filename:
                    import uuid
                    filename = f"image_{uuid.uuid4().hex[:8]}.png"

            target_path = self.images_dir / filename
            
            logger.info(f"Fetching image from {url} to {target_path}")
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, follow_redirects=True)
                response.raise_for_status()
                
                try:
                    with open(target_path, "wb") as f:
                        f.write(response.content)
                    logger.info(f"Successfully saved image to {target_path}")
                    # Return relative path for frontend access
                    return f"/static/images/{filename}"
                except (OSError, IOError) as e:
                    logger.warning(f"Could not save image locally: {e}")
                    return url # Return original URL as fallback
            
        except Exception as e:
            logger.error(f"Failed to fetch image from {url}: {str(e)}")
            raise Exception(f"Failed to fetch image: {str(e)}")

def get_utils_service() -> UtilsService:
    return UtilsService()
