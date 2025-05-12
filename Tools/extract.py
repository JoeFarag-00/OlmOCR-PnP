import os
from PyPDF2 import PdfReader

pdf_folder = "Input_PDFs"
output_folder = "Lawstxt"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(pdf_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        txt_path = os.path.join(output_folder, txt_filename)

        try:
            reader = PdfReader(pdf_path)
            all_text = ""
            for page in reader.pages:
                all_text += page.extract_text() or ""

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(all_text)

            print(f"✓ Converted: {filename} → {txt_filename}")
        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")
