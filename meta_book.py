# DEVELOPER TOOL
# Generates Librarian Sora's book index book

import os
import json
from collections import defaultdict
import re

# Directory containing the lore books
LORE_BOOKS_DIR = "lore_books"
META_INDEX_FILE = os.path.join(LORE_BOOKS_DIR, "Librarian Sora - The Book Index.json")

def extract_number(title):
    match = re.search(r'\d+', title)
    return int(match.group()) if match else float('inf')

def main():
    # Dictionary to store authors and their books
    author_books = defaultdict(list)

    # Iterate through all JSON files in the directory
    for filename in os.listdir(LORE_BOOKS_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(LORE_BOOKS_DIR, filename)

            # Load the book's JSON content
            with open(filepath, "r", encoding="utf-8") as file:
                try:
                    book_data = json.load(file)
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON file: {filename}")
                    continue

                # Extract title and author
                title = book_data.get("title", "Untitled")
                author = book_data.get("author", "Unknown Author")

                # Append the book title to the author's list
                author_books[author].append(title)

    # Create the meta-index book
    meta_index = {
        "title": "The Book Index",
        "author": "Librarian Sora",
        "pages": []
    }

    # Sort authors and their books alphabetically, considering numbers in titles
    for author in sorted(author_books):
        books = sorted(author_books[author], key=lambda title: (extract_number(title), title))
        page_content = [
            {"text": f"{author}:\n", "bold": True},
            {"text": "\n".join(f"- {book}" for book in books), "bold": False}
        ]
        meta_index["pages"].append(page_content)

    # Save the meta-index book as a JSON file
    with open(META_INDEX_FILE, "w", encoding="utf-8") as file:
        json.dump(meta_index, file, indent=4)

    print(f"Meta-index book generated and saved to {META_INDEX_FILE}")

if __name__ == "__main__":
    main()
