# Babel Book Loot v1.0
## A customisable pre-written book loot datapack for Minecraft

Babel Book Loot adds over 100 pre-written books to various loot tables in Minecraft. The default library of books is a collection of public domain fairy tales. You can customise the library by adding your own text files.

It was last updated for Minecraft 1.21.

## Quick-start

Download [babel_v1.0.zip](https://github.com/JiFish/babel/releases/download/v1.0/babel_v1.0.zip) and place it in your Minecraft world's datapack directory.

If you don't want zombies dropping books, download [babel-no-zombie-loot_v1.0.zip](https://github.com/JiFish/babel/releases/download/v1.0/babel-no-zombie-loot_v1.0.zip) instead.

## How the datapack works in-game

Written books can be dropped by zombies if killed by a player, or fished up with a fishing rod. They can also be found in villages, stronghold libraries and woodland mansions in chests.

The generation of the book is determined randomly:
- 69% Tattered Book
- 30% Copy of a copy
- 1% Copy of original
- <1% Original

## Customising Books

Run `py babel.py` (or `babel.exe` in windows.) this will output `babel.zip`. Put that file in your Minecraft world's datapack directory. Run `babel.py -h` to see more options.

Any books in the `books` directory will be included. You can add and remove books as you wish.

Book can be in JSON or YAML formats. Here is a simple example:

**sample_book.yaml**
```
title: Sample Book
author: Some Author
pages:
    - This is page one.
    - This is page two.
    - This is page three.
```

**sample_book.json:**
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

### Advanced Books

You can do more advanced stuff with books if you need it.

#### Colors, formatting, etc.

Your pages can be in [Raw JSON text format](https://minecraft.wiki/w/Raw_JSON_text_format) e.g.

```
{
    "title": "Sample Book",
    "author": "Some Author",
    "pages": [
        [{"text":"Hello ","color":"dark_red"},{"text":"World","bold":true},{"text":"!"}],
    ]
}
```

#### Optional parameters

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

### Submitting books
If you've made some books and the text is in the public domain, please consider submitting them back here!

### Default library
The default collection of books was sourced from Project Gutenberg. https://www.gutenberg.org/

### Updating books from v0.5
If you already have books in the v0.5 format, you can update them by running `update_books.py`. The books directory must only contain v0.5 format books. The script will also overwrite the originals, so keep a backup.

## Advanced Customisation
### Altering where books will be found
You can disable various book drops using command line options. Use `babel.py -h` to see the complete list. An example where zombies do not drop books:
```
babel.py -d zombie
````

You can add books to other loot tables using type `minecraft:loot_table` and value `babel:books`.

### Dealing with datapack conflicts
If any of your other datapacks modify loot tables used by babel, it might be possible to create a compatible pack. To do this, replace the loot tables in the `base_loot_tables` with the ones from the conflicting datapack. This isn't guaranteed to work, and won't if the tables are much different from expected.

### For use making your own datapacks
If you just want to generate the loot table without the surrounding files, try:
```
build_loottable.py > books.json
```

### Full argument list:
```
usage: babel.py [-h] [-v] [-d {fishing,village,mansion,stronghold,zombie}]
                [-i] [-!] [filename]

positional arguments:
  filename              Optional output zip filename. (default: babel.zip)

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -d {fishing,village,mansion,stronghold,zombie}
                        Disable adding books to the given loot tables. Can be
                        repeated to disable more than one.
  -i, --indent          Indent output JSON files.
  -!, --no-wait         Don't wait for user input when finished. Triggered
                        automatically by using any other argument. (Windows
                        version only.)
```

## Comments, suggestions or contributions?
Please use the Issue Tracker on GitHub, or send me a tweet [@JiFish](https://twitter.com/intent/tweet?text=.@JiFish) or Toot [@joe@social.jifish.co.uk](https://social.jifish.co.uk/@joe).

## Copyright & use in your own datapacks
Assuming the books are your own work, loot tables outputted by babel belong to you. You can use them freely in your own datapack. A credit is very appreciated, but not required.

Books in the `books` directory are in the public domain. The `books.json` file created from them is also in the public domain.

The babel tool and datapack is copyright Joseph Fowler.

## Disclaimer

Software provided is "as is", without a warranty, and should be used at your own risk.
