import logging
import sys
from app.core.config import get_settings

settings = get_settings()

def setup_logging():
    logger = logging.getLogger("ai_app")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = setup_logging()
