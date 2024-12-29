# By Joseph "JiFish" Fowler. All rights reserved.

import json
import yaml
import os
from progress_bar import printProgressBar
from sys import argv
from config import loadAndValidateYaml

# Use a YAML parser to decode books. This allows JSON, but also
# allows looser formatted JSON like the minecraft parser does.
# One place this fails is yaml expects a space after an unquoted key.
# This function attempts to fix these key/val pairs after decode.
# Only the top level is fixed, which is all that should be needed for this application.
def decode_book(directory, filename):
    try:
        path = os.path.join(directory, filename)
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
    except yaml.YAMLError as err:
        raise RuntimeError("Failed to parse book: %s. Check the markup is correct." % filename)

# Validate book. Books must have author, title and at least 1 page
def validate_book(filename, book):
    errors = []
    if 'author' not in book:
        errors.append("author not specified")
    elif type(book['author']) != str:
        errors.append("author is not a string")
    if 'title' not in book:
        errors.append("title not specified")
    elif type(book['title']) != str:
        errors.append("title is not a string")
    if 'pages' not in book:
        errors.append("pages not specified")
    elif type(book['pages']) != list:
        errors.append("pages is not a list")
    elif len(book['pages']) < 1:
        errors.append("pages is empty")
# TODO: page validation
#    else:
#        for i, p in enumerate(book['pages']):
#            if type(p) != str:
#                errors.append("page %s is not a string" % (i+1))

    if len(errors) > 0:
        raise RuntimeError("Validation problems in %s:\n- %s" % (filename, "\n- ".join(errors)))


def buildLootTable(config, progressBar=True):
    entries = []

    # Loop through the books directory and add them all
    directory = config['books-path']
    dirlist = os.listdir(directory)
    totalfiles = len(dirlist)

    # Pre-create generation chance functions, and figure out default generation
    generationChances = {
        2: config['copy-of-copy-chance'],
        1: config['copy-of-original-chance'],
        0: config['original-chance']
    }
    generationFunctions = []
    defaultGeneration = 3
    for generation, generationChance in generationChances.items():
        # If 1, this is the new default generation
        if generationChance == 1:
            defaultGeneration = generation
            # Clear out any previous functions so they don't overwrite the new default
            generationFunctions = []
        # Only add functions with a chance above 0
        elif generationChance > 0:
            generationFunctions.append({
                "function": "minecraft:set_book_cover",
                "generation": generation,
                "conditions": [
                    {
                        'condition': "random_chance",
                        'chance': generationChance
                    }
                ]
            })

    if totalfiles < 1:
        raise RuntimeError("No books were found!")

    if progressBar:
        print(f"Found {totalfiles} books in {directory}.")
        printProgressBar(0, totalfiles, prefix='Importing Books...', length=40, decimals=0)
    for i, file in enumerate(dirlist):
        book = decode_book(directory, file)
        validate_book(file, book)

        if 'weight' in book:
            weight = book['weight']
        else:
            weight = 1

        # Basic item and functions
        thisBook = {
            "type": "minecraft:item",
            "name": "minecraft:written_book",
            "weight": weight,
            "functions": [
                {
                    "function": "minecraft:set_written_book_pages",
                    "pages": book['pages'],
                    "mode": "replace_all"
                },
                {
                    "function": "minecraft:set_book_cover",
                    "author": book['author'],
                    "title": book['title'],
                    "generation": defaultGeneration,
                }
            ]
        }

        # Optional functions
        if "lore" in book:
            thisBook["functions"].append({
                "function": "minecraft:set_lore",
                "lore": book['lore'],
                "mode": "replace_all"
            })
        if "custom_data" in book:
            if type(book['custom_data']) == str:
                customData = book['customData']
            else:
                customData = json.dumps(book['customData'], ensure_ascii=False)
            thisBook["functions"].append({
                "function": "minecraft:set_custom_data",
                "tag": customData
            })

        # Append to entries
        entries.append(thisBook)
        if progressBar:
            printProgressBar(i + 1, totalfiles, prefix='Importing Books...', length=40, decimals=0)

    loottable = {
        'pools': [
            {
                'rolls': 1,
                'entries': entries,
                'functions': generationFunctions
            }
        ]
    }

    return loottable


if __name__ == '__main__':
    config = loadAndValidateYaml(argv[1] if argv[1] else 'config.yaml')
    loottable = buildLootTable(config, False)
    print(json.dumps(loottable, indent=2, ensure_ascii=False))
