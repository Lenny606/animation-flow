from app.repositories.base import BaseRepository
from app.models.scenario import Scenario
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
from app.db.mongodb import get_database

class ScenarioRepository(BaseRepository[Scenario]):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "scenarios", Scenario)

async def get_scenario_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> ScenarioRepository:
    return ScenarioRepository(db)
