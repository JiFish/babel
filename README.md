![Logo](readme_images/logo.png)

![Demo](readme_images/babel.gif)

# Babel Book Loot v1.1
## A customizable pre-written book loot data pack for Minecraft

Babel Book Loot adds over 100 pre-written books to various loot tables in Minecraft. The default library of books is a collection of public domain fairy tales. You can customize the library by adding your own books.

It was last updated for Minecraft 1.21.

## Quick-start

Download [babel_v1.1.zip](https://github.com/JiFish/babel/releases/download/v1.1/babel_v1.1.zip) and place it in your Minecraft world's `datapacks` directory.

## How the data pack works in-game

Written books can be dropped by zombies if killed by a player, or fished up with a fishing rod. They can also be found in villages, stronghold libraries and woodland mansions in chests.

The generation of the book is determined randomly:
- 33% Tattered Book (not copyable)
- 65% Copy of a copy (not copyable)
- 1% Copy of original
- <1% Original

If you are hero of the village, librarians throw a guaranteed copyable book.

## Pre-customized options

These data packs are variations with tweaked rules for obtaining the books:

- [babel-no-copying_v1.1.zip](https://github.com/JiFish/babel/releases/download/v1.1/babel-no-copying_v1.1.zip) - All books are "copy of a copy" and can't be duplicated. Also disables hero of the village reward.
- [babel-no-zombie-loot_v1.1.zip](https://github.com/JiFish/babel/releases/download/v1.1/babel-no-zombie-loot_v1.1.zip) - Zombies don't drop books.
- [babel-only-chests_v1.1.zip](https://github.com/JiFish/babel/releases/download/v1.1/babel-only-chests_v1.1.zip) - Books can only be found in chests. No zombie drops, fishing, or hero of the village reward.
- [babel-recipe_v1.1.zip](https://github.com/JiFish/babel/releases/download/v1.1/babel-recipe_v1.1.zip) - Includes the below recipe to craft random books.

#### Optional recipe

If you got the version with the crafting recipe. Just combine 1 Book and Quill, 1 Soul Sand Block, 1 Chest, and 1 Emerald. (The recipe is shapeless.) This gives a chest which once placed will have a single random book inside.

![Recipe Image](readme_images/optional_recipe.png)

## Advanced customization using Babel Builder Tool

First get babel-builder-windows_v1.1.zip or babel-builder-python_v1.1.zip from the [releases page](https://github.com/JiFish/babel/releases).

Run `py babel.py` (or `babel.exe` in windows.) this will output `babel.zip`. Put that file in your Minecraft world's `datapacks` directory.

### Changing included books

Any books in the `books` directory will be included. You can add and remove books as you wish.

Books can be in JSON or YAML formats. Here are some simple examples:

#### sample_book.yaml
```
title: Sample Book
author: Some Author
pages:
    - This is page one.
    - This is page two.
    - This is page three.
```

#### sample_book.json
```
{
    "title": "Sample Book",
    "author": "Some Author",
    "pages": [
        "This is page one.",
        "This is page two.",
        "This is page three."
    ]
}
```

Minecraft accepts strictly non-valid JSON, so babel tries to too. Babel does it's best to read the books, but if it's having issues your best bet is to ensure the file is valid JSON.

**Important note**: There is no easy way to find out how much text will fit on a page and Minecraft will allow pages longer than it can display. The simplest way to figure out the correct page lengths is to write the pages in minecraft itself, then copy the text out. [Text2Book](https://thewilley.github.io/Text2Book/) can assist you with splitting up your text.

**If you've made book files and the text is in the public domain, please consider submitting them back here!**

#### Colors, formatting, etc.

Your book pages can be in [Raw JSON text format](https://minecraft.wiki/w/Raw_JSON_text_format) e.g.

```
{
    "title": "Sample Book",
    "author": "Some Author",
    "pages": [
        [{"text":"Hello ","color":"dark_red"},{"text":"World","bold":true},{"text":"!"}],
    ]
}
```

#### Optional book parameters

Book files can contain the following optional parameters:
- `weight` - The chance this book will be selected vs others in the table. Default is `1`, so a value of `2` would mean the book is twice as likely to be selected.
- `lore` - Item lore text. Works like `pages`.
- `custom_model_data` - Sets item's custom_model_data value to allow the book a unique texture via a resource pack.
- `custom_data` - Sets item's custom data. Can be a string containing nbt tags, or the tags themselves.

An example using all optional parameters:

```
{
    "title": "Another Sample Book",
    "author": "Some Author",
    "pages": [
        "Hello World!",
    ],
    "weight": 2,
    "lore": [
        [{"text":"Lore line 1","color":"blue"}],
        "Lore line 2"
    ],
    "custom_model_data": 42,
    "custom_data": {
        "foo": "bar",
        "number": 16
    }
}
```

#### Updating books from v0.5
If you already have books in the v0.5 format, you can update them by running `update_books.py`. The books directory must only contain v0.5 format books. The script will also overwrite the originals, so keep a backup.

### Changing other pack settings

You can disable various loot drops, change generation chances, and make other customizations by editing `config.yaml`.

### Full argument list:
```
usage: babel.py [-h] [-v] [-!] [-i] [-a] [filename]

positional arguments:
  filename              Configuration filename. (default: config.yaml)

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -!, --no-wait         Don't wait for user input when finished. (Windows version only.)
  -i, --indent          Indent output json files. Overrides config field.
  -a, --append-version  Append babel version number to output filename.
```

## Use with other data packs

### Using as part of your own data packs
You can add books to other loot tables using type `minecraft:loot_table` and value `babel:books`.

If you just want to generate the loot table without the surrounding files, try running: `py build_loottable.py > books.json`

### Dealing with data pack conflicts
If any of your other data packs modify loot tables used by babel, it might be possible to create a compatible pack. To do this, replace the loot tables in the `data/base_loot_tables` with the versions from the conflicting data pack. Then make sure this data pack is loaded before the conflicting one. This isn't guaranteed to work, and won't if the tables are much different from expected.

## Comments, suggestions or contributions?
Please use the Issue Tracker on GitHub, or send me a tweet [@JiFish](https://twitter.com/intent/tweet?text=.@JiFish) or Toot [@joe@social.jifish.co.uk](https://social.jifish.co.uk/@joe).

## Copyright & use in your own data packs
Assuming the books are your own work, loot tables outputted by babel belong to you. You can use them freely in your own data pack. A credit is very appreciated, but not required.

Books in the `books` directory are in the public domain, sourced from [Project Gutenberg](https://www.gutenberg.org/). The `books.json` file created from them is also in the public domain.

The babel tool and data pack is copyright Joseph Fowler.

## Disclaimer

Software provided is "as is", without a warranty, and should be used at your own risk.
