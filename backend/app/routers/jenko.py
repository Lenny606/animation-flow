from fastapi import APIRouter, Depends, HTTPException, status
from app.db.mongodb import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.image_data import ImageData

router = APIRouter(
    prefix="/jenko",
    tags=["jenko"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ImageData)
async def create_image_data(image_data: ImageData, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Save image data to the database.
    """
    # Exclude _id from invalid data if it's there (though pydantic might handle it, better be safe)
    # The user provides filename, title, desc. Created_at is default. ID is None.
    
    data_dict = image_data.model_dump(by_alias=True, exclude={"id"})
    
    try:
        new_image = await db.image_data.insert_one(data_dict)
        created_image = await db.image_data.find_one({"_id": new_image.inserted_id})
        
        # Convert _id to string for response
        if created_image:
           created_image["_id"] = str(created_image["_id"])
           
        return created_image
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export", response_model=list[ImageData])
async def export_image_data(db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Get all image data from the database.
    If multiple entries with the same filename exist, only the newest one is returned.
    """
    try:
        pipeline = [
            {"$sort": {"created_at": -1}},  # Sort descending by creation time
            {
                "$group": {
                    "_id": "$filename",  # Group by filename
                    "newest_doc": {"$first": "$$ROOT"}  # Take the first (newest) document in each group
                }
            },
            {"$replaceRoot": {"newRoot": "$newest_doc"}},
            {"$sort": {"created_at": -1}}  # Final sort for results
        ]
        
        cursor = db.image_data.aggregate(pipeline)
        images = await cursor.to_list(length=1000)
        
        # Convert _id to string for each document
        for image in images:
            image["_id"] = str(image["_id"])
            
        return images
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

