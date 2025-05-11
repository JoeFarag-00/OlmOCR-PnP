import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(BASE_DIR, "Input_PDFs")
CHUNK_FOLDER = os.path.join(BASE_DIR, "Chunked_PDFs")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "Output_PDFs")
OLMOCR_URL = "https://olmocr.allenai.org/"
HEADLESS_MODE = True

MAX_WAIT_TIME_PAGE_LOAD = 20
MAX_WAIT_TIME_ACCEPT_BTN = 7
MAX_WAIT_TIME_UPLOAD_ELEMENT = 20
MAX_WAIT_TIME_PROCESS_BTN_APPEAR = 20
MAX_WAIT_TIME_PROCESSING_START_INDICATOR = 60
MAX_WAIT_TIME_PROCESSING_FINISH_BTN = 600

LOG_FILE_NAME = "ingestion_process.log"
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - Line %(lineno)d - %(message)s'