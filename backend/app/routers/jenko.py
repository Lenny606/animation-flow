from fastapi import APIRouter, Depends, status, Request
from app.models.image_data import ImageData
from app.core.rate_limit import limiter, get_role_limit
from app.repositories.image_data_repository import ImageDataRepository, get_image_data_repository
from app.core.error_handling import InternalServerException

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ImageData, summary="Save image data", description="Stores metadata about a generated or uploaded image in the database.")
@limiter.limit(get_role_limit("5/minute", "20/minute", "100/minute"))
async def create_image_data(
    request: Request, 
    image_data: ImageData, 
    image_data_repo: ImageDataRepository = Depends(get_image_data_repository)
):
    """
    Save image data to the database.
    """
    try:
        return await image_data_repo.create(image_data)
    except Exception as e:
        raise InternalServerException(detail=f"Failed to create image data: {str(e)}")

@router.get("/export", response_model=list[ImageData], summary="Export image data", description="Retrieves all stored image metadata. If multiple entries exist for the same filename, only the most recent one is returned.")
@limiter.limit(get_role_limit("10/minute", "50/minute", "200/minute"))
async def export_image_data(
    request: Request, 
    image_data_repo: ImageDataRepository = Depends(get_image_data_repository)
):
    """
    Get all image data from the database.
    If multiple entries with the same filename exist, only the newest one is returned.
    """
    try:
        return await image_data_repo.get_newest_per_filename()
    except Exception as e:
        raise InternalServerException(detail=f"Failed to export image data: {str(e)}")

