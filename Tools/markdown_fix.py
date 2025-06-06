import os
import re
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq, APIStatusError
from tqdm import tqdm

env_loaded = load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("🔑 GROQ_API_KEY not found in .env")

client = Groq(api_key=API_KEY)
MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
TOKEN_LIMIT = 5000  

INPUT_DIR = Path("Output_PDFs")
OUTPUT_DIR = Path("Output_Cleaned")
OUTPUT_DIR.mkdir(exist_ok=True)

PROMPT = """
You are a Markdown-cleaning assistant. Given the raw Markdown content, do the following:
1. Fix any incorrect, incomplete, or typo-ridden sentences (in both English and Arabic).
2. Convert all <p>-wrapped bullet blocks into a proper HTML list:
   <ul><li>…</li><li>…</li></ul>
3. Fill in any missing letters or words so it reads naturally.
4. If the markdown needs no change, then return the same markdown unedited.

Return ONLY the cleaned Markdown.
""".strip()

SPLITTER_PATTERN = re.compile(r"(?:^|\n)(---\s*Page Break\s*---|=== Chunk Break ===)(?:\n|$)", re.IGNORECASE)
REMOVE_MARKERS = re.compile(r"---\s*Page Break\s*---|=== Chunk Break ===", re.IGNORECASE)

def approx_tokens(text: str) -> int:
    return int(len(text.split()) / 0.75)

def split_into_groups(text: str, max_tokens: int) -> list[str]:
    parts = SPLITTER_PATTERN.split(text)
    groups, current = [], ""
    for piece in parts:
        if approx_tokens(current + piece) <= max_tokens or not current:
            current += piece
        else:
            groups.append(current)
            current = piece
    if current:
        groups.append(current)
    return groups

def call_groq(chunk: str) -> str:
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": PROMPT + "\n\n" + chunk}],
            stream=False,
        )
        return resp.choices[0].message.content
    except APIStatusError as e:
        raise


def clean_file(path: Path):
    raw = path.read_text(encoding="utf-8")
    # Determine if splitting needed
    needs_split = approx_tokens(raw) > TOKEN_LIMIT
    chunks = [raw]
    if needs_split:
        print(f"⚠️ {path.name} exceeds token limit, splitting into chunks…")
        chunks = split_into_groups(raw, TOKEN_LIMIT)

    cleaned_parts = []
    for chunk in tqdm(chunks, desc=f"Cleaning {path.name}"):
        try:
            cleaned_parts.append(call_groq(chunk))
        except APIStatusError as e:
            print(f"  ⚠️ Chunk too large or rate limited, splitting further…")
            subchunks = split_into_groups(chunk, TOKEN_LIMIT // 2)
            for sub in tqdm(subchunks, desc="Sub-chunks", leave=False):
                cleaned_parts.append(call_groq(sub))
    cleaned = "\n".join(cleaned_parts)
    cleaned = REMOVE_MARKERS.sub("", cleaned)

    output_path = OUTPUT_DIR / path.name
    output_path.write_text(cleaned, encoding="utf-8")
    print(f"✅ Cleaned {path.name} -> {output_path}")

def main():
    txts = list(INPUT_DIR.glob("*.txt"))
    if not txts:
        print("No .txt files found in input directory.")
        return
    for txt in tqdm(txts, desc="Processing text files"):
        clean_file(txt)

if __name__ == "__main__":
    main()