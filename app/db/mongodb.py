from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()

class MongoDB:
    client: AsyncIOMotorClient = None

    def connect(self):
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise

    def close(self):
        if self.client:
            self.client.close()
            logger.info("Closed MongoDB connection")

db = MongoDB()

async def get_database():
    return db.client[settings.DATABASE_NAME]
