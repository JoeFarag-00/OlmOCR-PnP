import os
import logging
from pathlib import Path
from config import LOG_FILE_NAME, LOG_FORMAT

logger = logging.getLogger('OlmOCR_Ingester')

def setup_file_logging():
    logger.setLevel(logging.INFO)
    if logger.hasHandlers():
        logger.handlers.clear()
    log_dir = Path(__file__).resolve().parent
    log_path = log_dir / LOG_FILE_NAME
    os.makedirs(log_dir, exist_ok=True)
    handler = logging.FileHandler(log_path, mode='a')
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(handler)