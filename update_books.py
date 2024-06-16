# Script to upgrade a books directory from v0.5 format to v1.0 format. Only works with valid JSON format books.
# Warning 1: The script will also overwrite the originals, so keep a backup.
# Warning 2: The script will break if v1.0 format books are present in books directory.

import os
import json

# Directory containing the JSON files
directory = 'books/';

# Function to decode the pages in a JSON file
def decode_pages(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Decode each page
    decoded_pages = [json.loads(page) for page in data['pages']]
    
    # Update the pages with the decoded content
    data['pages'] = decoded_pages
    
    # Save the updated content back to the same file with indentation
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
        file.write('\n')  # Ensure there is a newline at the end of the file

# Iterate over all JSON files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        file_path = os.path.join(directory, filename)
        decode_pages(file_path)
        print(f'Processed {file_path}')
