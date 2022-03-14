import json
import yaml
import os
import sys

isCompiled = getattr(sys, 'frozen', False)

directory = 'books/'
entries = [];

# Use a YAML parser to decode books. This allows JSON, but also
# allows looser formated JSON like the minecraft parser does.
# One place this fails is yaml expects a space after an unquoted key.
# This function attempts to fix these key/val pairs after decode.
# Only the top level is fixed, which is all that should be needed for this application.
def decode_book(filename):
    try:
        path = os.path.join(directory, file)
        with open(path, 'r', encoding="utf-8") as thisfile:
            book = thisfile.read()
        book = yaml.safe_load(book)
        
        # Fix mis-decoded key/val
        keylist = book.keys()
        for key in keylist:
            if ":" in key:
                newkey, val = key.split(":")
                del book[key]
                book[newkey] = val
                
        return book
    except:
        print("\nFailed to parse book: "+filename+". Check the markup is correct.")
        if isCompiled:
            input("\nPress ENTER or close this window.")
        exit(1)
        
# Validate book. Books must have author, title and at least 1 page
def validate_book(filename, book):
    error = False
    if 'author' not in book:
        error = True
        print("author not specified in "+filename)
    elif type(book['author']) != str:
        error = True
        print("author is not a string in "+filename)
    if 'title' not in book:
        error = True
        print("title not specified in "+filename)
    elif type(book['title']) != str:
        error = True
        print("title is not a string in "+filename)
    if 'pages' not in book:
        error = True
        print("pages not specified in "+filename)
    elif type(book['pages']) != list:
        error = True
        print("pages is not a list in "+filename)
    elif len(book['pages']) < 1:
        error = True
        print("pages is empty in "+filename)
    else:
        for p in book['pages']:
            if type(p) != str:
                error = True
                print("single page is not a string in "+filename)
                
    if error:
        if isCompiled:
            input("\nPress ENTER or close this window.")
        exit(1)

# Loop through the books directory and add them all
for file in os.listdir(directory):
    book = decode_book(file)
    validate_book(file, book)
    
    # Generation 3 by default, but this can be replaced
    book['generation'] = 3

    entries.append({
        "type": "item",
        "name": "minecraft:written_book",
        "weight": 1,
        "functions": [
            {
                "function": "minecraft:set_nbt",
                "tag": json.dumps(book, ensure_ascii=False)
            },
            {
                "function": "minecraft:set_nbt",
                "tag": json.dumps({'generation':2}),
                "conditions": [
                    {
                        'condition': "random_chance",
                        'chance': 0.3
                    }
                ]
            },
            {
                "function": "minecraft:set_nbt",
                "tag": json.dumps({'generation':1}),
                "conditions": [
                    {
                        'condition': "random_chance",
                        'chance': 0.01
                    }
                ]
            },
            {
                "function": "minecraft:set_nbt",
                "tag": json.dumps({'generation':0}),
                "conditions": [
                    {
                        'condition': "random_chance",
                        'chance': 0.003
                    }
                ]
            }
        ]
    })


loottable = {
    'pools': [
        {
            'rolls': 1,
            'entries': entries
        }
    ]
}

if __name__ == '__main__':
    print(json.dumps(loottable, indent=4, ensure_ascii=False))
