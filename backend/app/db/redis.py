import redis.asyncio as redis
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()

class RedisClient:
    client: redis.Redis = None

    async def connect(self):
        try:
            self.client = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
            await self.client.ping()
            logger.info("Connected to Redis")
        except Exception as e:
            logger.error(f"Could not connect to Redis: {e}")

    async def close(self):
        if self.client:
            await self.client.close()
            logger.info("Closed Redis connection")

redis_client = RedisClient()

async def get_redis():
    return redis_client.client
