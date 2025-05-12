import os
import re

directory = 'Output_PDFs'

new_splitter = '\n♦♦♦\n'

tag_patterns = [
    r'---\s*\n\s*Page Break\s*\n\s*---',       
    r'===\s*Chunk Break\s*===',                
]

combined_pattern = re.compile('|'.join(tag_patterns), flags=re.IGNORECASE)

for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        new_content = combined_pattern.sub(new_splitter, content)

        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"✅ Tags replaced in: {filename}")
        else:
            print(f"ℹ️  No tags found in: {filename}")

print("\n🎯 Tag replacement complete.")
