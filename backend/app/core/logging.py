import logging
import sys
from app.core.config import get_settings

settings = get_settings()

import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger("ai_app")
    logger.setLevel(logging.DEBUG)

    # Clear existing handlers to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    # Console Handler
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # File logging (optional, skip if on read-only filesystem like Vercel)
    try:
        log_file = settings.LOG_FILE_PATH
        log_dir = os.path.dirname(log_file)
        
        # Only attempt to create log directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # File Handler
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Error File Handler
        error_log_file = settings.ERROR_LOG_FILE_PATH
        error_file_handler = RotatingFileHandler(
            error_log_file, maxBytes=10*1024*1024, backupCount=5
        )
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(formatter)
        logger.addHandler(error_file_handler)
        
    except (OSError, IOError) as e:
        # On some environments like Vercel, the filesystem is read-only
        logger.warning(f"File logging disabled: {e}")

    return logger

logger = setup_logging()
