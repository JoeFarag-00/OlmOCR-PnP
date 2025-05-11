import os
import logging
from config import OUTPUT_FOLDER, LOG_FILE_NAME, LOG_FORMAT

logger = logging.getLogger('OlmOCR_Ingester')

def setup_file_logging():
    logger.setLevel(logging.INFO)
    if logger.hasHandlers():
        logger.handlers.clear()
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    handler = logging.FileHandler(os.path.join(OUTPUT_FOLDER, LOG_FILE_NAME), mode='a')
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(handler)