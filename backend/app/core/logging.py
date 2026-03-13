import logging
import sys
from app.core.config import get_settings

settings = get_settings()

import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger("ai_app")
    logger.setLevel(logging.DEBUG)

    # Console Handler
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # File Handler
    log_file = settings.LOG_FILE_PATH
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

logger = setup_logging()
