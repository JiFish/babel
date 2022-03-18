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
    else:
        for i, p in enumerate(book['pages']):
            if type(p) != str:
                errors.append("page %s is not a string" % (i+1))

    if len(errors) > 0:
        raise RuntimeError("Validation problems in %s:\n- %s" % (filename, "\n- ".join(errors)))

## https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

# Loop through the books directory and add them all
dirlist = os.listdir(directory)
totalfiles = len(dirlist)

if totalfiles < 1:
    raise RuntimeError("No books were found!")

printProgressBar(0, totalfiles, prefix='Importing Books...', length=35, decimals=0)
for i, file in enumerate(dirlist):
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
    printProgressBar(i+1, totalfiles, prefix='Importing Books...', length=35, decimals=0)


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
