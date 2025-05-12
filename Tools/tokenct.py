import os
import argparse
import pandas as pd

DEFAULT_INPUT_DIR = 'Output_PDFs'
DEFAULT_OUTPUT_DIR = 'Tools'


def count_tokens(text: str) -> int:

    return sum(1 for c in text if not c.isspace())


def process_text(text: str):

    sections = text.split('♦♦♦')
    return [count_tokens(sec) for sec in sections]


def gather_txt_files(input_dir):
    """
    Return all .txt file paths in the input directory.
    """
    if not os.path.isdir(input_dir):
        return []
    return [os.path.join(input_dir, f)
            for f in os.listdir(input_dir)
            if f.lower().endswith('.txt')]


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate token stats from .txt files in a folder and export to Excel."
    )
    parser.add_argument(
        '--input', '-i',
        default=DEFAULT_INPUT_DIR,
        help=f"Path to folder containing .txt files (default: {DEFAULT_INPUT_DIR})"
    )
    parser.add_argument(
        '--output', '-o',
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory where the Excel file will be saved (default: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        '--outfile', '-f',
        default='token_stats.xlsx',
        help="Excel file name (default: token_stats.xlsx)"
    )
    args = parser.parse_args()

    files = gather_txt_files(args.input)
    if not files:
        print(f"No .txt files found in '{args.input}'")
        return

    stats = [] 
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

        counts = process_text(text)
        if not counts:
            continue

        stats.append({
            'file': os.path.basename(file_path),
            'max_tokens': max(counts),
            'min_tokens': min(counts),
            'avg_tokens': sum(counts) / len(counts)
        })

    df = pd.DataFrame(stats)
    os.makedirs(args.output, exist_ok=True)
    output_path = os.path.join(args.output, args.outfile)
    try:
        df.to_excel(output_path, index=False)
        print(f"Stats written to '{output_path}'")
    except Exception as e:
        print(f"Failed to write Excel file: {e}")


if __name__ == '__main__':
    main()