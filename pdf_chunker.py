import os
from tqdm import tqdm
from PyPDF2 import PdfReader, PdfWriter
from config import INPUT_FOLDER, CHUNK_FOLDER
from logger import logger

class PDFChunker:
    def __init__(self, chunk_size=10):
        self.chunk_size = chunk_size
        os.makedirs(CHUNK_FOLDER, exist_ok=True)

    def _chunk_file(self, fname):
        path = os.path.join(INPUT_FOLDER, fname)
        reader = PdfReader(path)
        total = len(reader.pages)
        parts = ((total - 1) // self.chunk_size) + 1
        base = os.path.splitext(fname)[0]

        for i in range(parts):
            writer = PdfWriter()
            start = i * self.chunk_size
            end = min(start + self.chunk_size, total)
            for page in reader.pages[start:end]:
                writer.add_page(page)
            chunk_name = f"{base}_part{i+1}.pdf"
            out_path = os.path.join(CHUNK_FOLDER, chunk_name)
            with open(out_path, 'wb') as out_f:
                writer.write(out_f)
        logger.info(f"Chunked '{fname}' into {parts} parts.")

    def chunk_all(self):
        files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith('.pdf')]
        for fname in tqdm(files, desc="Chunking PDFs", unit="file"):
            self._chunk_file(fname)