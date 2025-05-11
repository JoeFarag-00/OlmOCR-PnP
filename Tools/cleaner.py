import os
import re
import pandas as pd

# Define allowed characters
allowed_pattern = re.compile(r'[A-Za-z0-9\u0600-\u06FF\s.,;:!?(){}\[\]\'"@#$%^&*+=<>|\\/~`_-]')

# Directory with text files
directory = 'Output_PDFs'  # change as needed

# Track edits
edit_log = []

# Loop through all text files
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        cleaned_content = ''
        removed_chars = set()

        for char in content:
            if allowed_pattern.match(char):
                cleaned_content += char
            else:
                removed_chars.add(char)

        # Only rewrite the file if something was removed
        if removed_chars:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_content)
            
            edit_log.append({
                'filename': filename,
                'removed_characters': ''.join(sorted(removed_chars))
            })

# Save results to Excel
if edit_log:
    df = pd.DataFrame(edit_log)
    df.to_excel('Tools/cleaning_report.xlsx', index=False)
    print("Cleaning complete. See 'cleaning_report.xlsx' for details.")
else:
    print("No non-English/Arabic/Markdown characters found. All files are clean.")
