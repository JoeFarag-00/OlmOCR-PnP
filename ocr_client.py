import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config import OLMOCR_URL, HEADLESS_MODE, MAX_WAIT_TIME_PAGE_LOAD, MAX_WAIT_TIME_ACCEPT_BTN, MAX_WAIT_TIME_UPLOAD_ELEMENT, MAX_WAIT_TIME_PROCESS_BTN_APPEAR,MAX_WAIT_TIME_PROCESSING_FINISH_BTN
from logger import logger

class OCRClient:
    def __init__(self):
        self.driver = self._setup_driver()
        self._goto_home()

    def _setup_driver(self):
        opts = Options()
        if HEADLESS_MODE:
            opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1920x1080")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=opts)
        driver.set_page_load_timeout(MAX_WAIT_TIME_PAGE_LOAD)
        return driver

    def _goto_home(self):
        self.driver.get(OLMOCR_URL)
        self._accept_terms()

    def _accept_terms(self):
        try:
            btn = WebDriverWait(self.driver, MAX_WAIT_TIME_ACCEPT_BTN).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Accept']"))
            )
            btn.click()
            time.sleep(1)
        except Exception:
            pass

    def process(self, pdf_path):
        try:
            inp = WebDriverWait(self.driver, MAX_WAIT_TIME_UPLOAD_ELEMENT).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            inp.send_keys(pdf_path)
            self.driver.find_element(By.XPATH,
                "//button[normalize-space()='Process Document' and not(@disabled)]").click()
            WebDriverWait(self.driver, MAX_WAIT_TIME_PROCESSING_FINISH_BTN).until(
                EC.element_to_be_clickable((By.XPATH,
                    "//button[normalize-space()='Process Document' and not(@disabled)]"))
            )
            time.sleep(2)

            buttons = self.driver.find_elements(By.XPATH,
                "//div[contains(@class,'css-lffl6r')]//button[contains(.,'Copy')]")
            texts = []
            for btn in buttons:
                btn.click(); time.sleep(0.6)
                txt = pyperclip.paste().strip()
                if txt:
                    texts.append(txt)
            return "\n\n---\nPage Break\n---\n\n".join(texts)
        except Exception as e:
            logger.error(f"OCR error for {pdf_path}: {e}", exc_info=True)
            return None

    def close(self):
        self.driver.quit()