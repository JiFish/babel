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

def buildBookEntry(book, defaultGeneration=0):
    thisBook = {
        "type": "minecraft:item",
        "name": "minecraft:written_book",
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

    # Optional parameters
    if "weight" in book:
        thisBook["weight"] = book["weight"]
    if "lore" in book:
        thisBook["functions"].append({
            "function": "minecraft:set_lore",
            "lore": book['lore'],
            "mode": "replace_all"
        })
    if "custom_data" in book:
        customData = book['custom_data'] if isinstance(book['custom_data'], str) else json.dumps(book['custom_data'], ensure_ascii=False)
        thisBook["functions"].append({
            "function": "minecraft:set_custom_data",
            "tag": customData
        })

    return thisBook

def buildLootTable(config, progressBar='Creating main loot table...'):
    directory = config['books-path']
    dirlist = os.listdir(directory)
    totalfiles = len(dirlist)

    if totalfiles < 1:
        raise RuntimeError("No books were found!")

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

    # Loop through the books directory and add them all
    entries = []
    if progressBar:
        print(f"Found {totalfiles} books in {directory}.")
        printProgressBar(0, totalfiles, prefix=progressBar, length=40, decimals=0)
    for i, file in enumerate(dirlist):
        book = decode_book(directory, file)
        validate_book(file, book)
        thisBook = buildBookEntry(book, defaultGeneration)
        entries.append(thisBook)
        if progressBar:
            printProgressBar(i + 1, totalfiles, prefix=progressBar, length=40, decimals=0)

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

def buildTestLootTables(config, progressBar=True):
    directory = config['books-path']
    dirlist = os.listdir(directory)
    totalfiles = len(dirlist)

    if totalfiles < 1:
        raise RuntimeError("No books were found!")

    entries = []
    if progressBar:
        printProgressBar(0, totalfiles, prefix='Creating test loot tables (metabox)...', length=40, decimals=0)
    for i, file in enumerate(dirlist):
        book = decode_book(directory, file)
        validate_book(file, book)
        thisBook = buildBookEntry(book)
        entries.append(thisBook)
        if progressBar:
            printProgressBar(i + 1, totalfiles, prefix='Creating test loot tables (metabox)...', length=40, decimals=0)

    # Split entries into multiple loot tables with up to 27 pools each
    lootTables = {}
    tableNum = 0
    for i in range(0, len(entries), 27):
        pools = [{'rolls': 1, 'entries': [entry]} for entry in entries[i:i + 27]]
        tableNum += 1
        lootTables[f"test_books_{tableNum}"] = {'pools': pools}

    # Meta box
    metaBoxPools = []
    for name in lootTables:
        metaBoxPools.append({
            "rolls": 1,
            "entries": [
                {
                    "type": "minecraft:item",
                    "name": "minecraft:light_gray_shulker_box"
                }
            ],
            "functions": [
                {
                    "function": "minecraft:set_name",
                    "name": lootTables[name]['pools'][0]["entries"][0]["functions"][1]["author"] +
                            " - " + lootTables[name]['pools'][-1]["entries"][0]["functions"][1]["author"]
                },
                {
                    "function": "minecraft:set_loot_table",
                    "type": "minecraft:shulker_box",
                    "name": f"babel:{name}"
                }
            ]
        })
    lootTables['metabox'] = {'pools':metaBoxPools}

    return lootTables


if __name__ == '__main__':
    config = loadAndValidateYaml(argv[1] if len(argv) > 1 else 'config.yaml')
    loottable = buildLootTable(config, False)
    print(json.dumps(loottable, indent=2, ensure_ascii=False))
