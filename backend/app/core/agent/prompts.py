import os
import yaml
from typing import Optional, Dict
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
from app.models.prompt_template import CustomPrompt
from app.db.mongodb import get_database
from app.core.logging import logger

# Base directory for prompt files
PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "prompts")

class PromptService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self._cache: Dict[str, str] = {}

    async def get_template(self, name: str, force_reload: bool = False) -> str:
        """
        Retrieves a prompt template. 
        Checks:
        1. Memory cache (if not force_reload).
        2. DB (MongoDB) for a custom override.
        3. File system (prompts/ directory) for the base version.
        """
        # 1. Check Cache
        if not force_reload and name in self._cache:
            return self._cache[name]

        # 2. Check DB Override
        try:
            if self.db is not None:
                db_prompt = await self.db.prompts.find_one({"name": name})
                if db_prompt:
                    template = db_prompt["template_text"]
                    self._cache[name] = template
                    return template
        except Exception as e:
            # We don't want to log timeout errors every time if DB is down
            # logger.error(f"Error fetching prompt '{name}' from DB: {e}")
            pass

        # 3. Load from File
        file_path = os.path.join(PROMPTS_DIR, f"{name}.yaml")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    data = yaml.safe_load(f)
                    template = data.get("template_text", "")
                    if template:
                        self._cache[name] = template
                        return template
            except Exception as e:
                logger.error(f"Error loading prompt file '{file_path}': {e}")

        logger.warning(f"Prompt template '{name}' not found in DB or file system.")
        return ""

    async def get_story_outline_template(self) -> str:
        return await self.get_template("story_outline")

    async def get_scene_scripting_template(self) -> str:
        return await self.get_template("scene_scripting")

async def get_prompt_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> PromptService:
    return PromptService(db)
