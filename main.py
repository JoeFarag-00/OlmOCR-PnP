import os
from collections import defaultdict
from tqdm import tqdm
from config import CHUNK_FOLDER, OUTPUT_FOLDER
from logger import setup_file_logging, logger   # pull in your logger
from pdf_chunker import PDFChunker
from ocr_client import OCRClient

class main:
    def __init__(self):
        setup_file_logging()
        self.chunker = PDFChunker()
        self.ocr = OCRClient()

    def run(self):
        self.chunker.chunk_all()

        chunks = sorted(os.listdir(CHUNK_FOLDER))
        groups = defaultdict(list)
        for fname in chunks:
            base = fname.rsplit('_part', 1)[0]
            groups[base].append(os.path.join(CHUNK_FOLDER, fname))

        for base, paths in tqdm(groups.items(), desc="PDFs", unit="pdf"):
            out_txt = os.path.join(OUTPUT_FOLDER, f"{base}.txt")

            if os.path.exists(out_txt):
                logger.info(f"Skipping '{base}' – '{base}.txt' already exists.")
                continue

            collected = []
            for p in tqdm(paths, desc=f"Chunks for {base}", unit="chunk", leave=False):
                text = self.ocr.process(os.path.abspath(p))
                if text:
                    collected.append(text)

            if collected:
                os.makedirs(OUTPUT_FOLDER, exist_ok=True)
                with open(out_txt, 'w', encoding='utf-8') as f:
                    f.write("\n\n=== Chunk Break ===\n\n".join(collected))
                logger.info(f"Wrote OCR output to '{out_txt}'")

        self.ocr.close()

if __name__ == '__main__':
    main().run()
