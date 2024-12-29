# Babel Book Loot v2.0-bleeding-edge

## Overview
Babel Book Loot is a customizable Minecraft data pack that adds over 130 pre-written lore books to various loot tables. You can expand the library by adding your own books. The pack is compatible with Minecraft 1.21.4 and likely works with older versions.

![Logo](readme_images/logo.png)

![Demo](readme_images/babel.gif)

## Quick Start
1. **Download the Data Pack**: [Download babel_v1.2.1.zip](https://github.com/JiFish/babel/releases/download/v1.1/babel_v1.2.1.zip).
2. **Install**: Place the downloaded `.zip` file in your Minecraft world's `datapacks` directory.

## Gameplay Features
- **Book Sources**: Find books in village and stronghold chests, woodland mansions, fish them up, or get them from a librarian as a raid reward. The pack also introduces a new structure, the Lost Library, filled with book-related loot.
- **Books to be found**: Includes lore, mechanics, fiction, and more, written by "in-universe" authors.
- **Book Rarity**:
  - 4.7%: Tattered Book (not copyable)
  - 90%: Copy of a copy (not copyable)
  - 5%: Copy of original
  - 0.3%: Original

  (Some loot, such as raid reward uses different values.)

## Pre-Customized Versions
Additional variations of the pack offer tweaked mechanics:
- **[babel-bookish-zombies_v1.2.1.zip](https://github.com/JiFish/babel/releases/download/v1.2.1/babel-bookish-zombies_v1.1.zip)**: Zombies can drop books when killed by a player.
- **[babel-only-chests_v1.2.1.zip](https://github.com/JiFish/babel/releases/download/v1.1/babel-only-chests_v1.1.zip)**: Books are chest-exclusive (no fishing or raid reward).
- **[babel-recipe_v1.2.1.zip](https://github.com/JiFish/babel/releases/download/v1.1/babel-recipe_v1.1.zip)**: Adds a crafting recipe for random books.
- **[babel-no-libraries_v2-be]()**: Removes Lost Libraries.
- **[babel-fairytales_v2-be]()**: Replaces lore books with public domain fairy tales.

#### Optional Crafting Recipe
If enabled, you can craft random books using: 1 Book and Quill, 1 Soul Sand Block, 1 Chest, and 1 Emerald. This recipe is shapeless and outputs a chest containing a single random book.

![Recipe Image](readme_images/optional_recipe.png)

## Advanced Customization with Babel Builder
The Babel Builder tool lets you customize your pack further:

1. **Download the Tool**:
   - [babel-builder-windows_v1.1.zip](https://github.com/JiFish/babel/releases) (Windows)
   - [babel-builder-python_v1.1.zip](https://github.com/JiFish/babel/releases) (Python)
2. **Run the Tool**:
   - Windows: `babel.exe`
   - Python: `python babel.py`
3. **Install Output**: Place the generated `babel.zip` in your Minecraft world's `datapacks` directory.

### Customizing Books
Books are stored in the `lore_books` directory, which can be changed via the `books-path` setting in the configuration file.

Books can be written in JSON or YAML formats. For example:

#### YAML Example
```yaml
title: Sample Book
author: Some Author
pages:
  - This is page one.
  - This is page two.
  - This is page three.
```

#### JSON Example
```json
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

Minecraft accepts slightly non-standard JSON, and Babel does its best to handle these formats. To ensure proper formatting, write pages directly in Minecraft or use tools like [Text2Book](https://thewilley.github.io/Text2Book/).

### Optional Book Attributes
Books can include additional attributes:
- **`weight`**: Affects selection probability (default: `1`).
- **`lore`**: Adds lore text, similar to `pages`.
- **`custom_data`**: Adds custom NBT tags.

Example with optional parameters:
```json
{
  "title": "Another Sample Book",
  "author": "Some Author",
  "pages": ["Hello World!"],
  "weight": 2,
  "lore": [[{"text":"Lore line 1","color":"blue"}], "Lore line 2"],
  "custom_data": {"foo": "bar", "number": 16}
}
```

### Configurable Settings
Edit `config.yaml` to:
- Disable specific loot drops.
- Adjust generation chances.
- Modify other pack settings.

### Full Command Options
```
usage: python babel.py [-h] [-v] [-!] [-i] [-a] [filename]

positional arguments:
  filename              Configuration filename (default: config.yaml)

optional arguments:
  -h, --help            Show help message and exit.
  -v, --version         Show version and exit.
  -!, --no-wait         Skip user input prompt (Windows only).
  -i, --indent          Indent JSON files (overrides config).
  -a, --append-version  Append version to output filename.
  -c, --chance-calc     Calculate book generation chances and exit.
```

## Using with Other Data Packs
### Integrating Books into Other Packs
Add books to custom loot tables using:
```json
{
  "type": "minecraft:loot_table",
  "value": "babel:books"
}
```

If you just want to generate the loot table without the surrounding files, try running:

```bash
python build_loottable.py config.yaml > books.json
```

## Contributions
- Submit issues or suggestions on GitHub.
- Reach out via Mastodon: [@joe@social.jifish.co.uk](https://social.jifish.co.uk/@joe).

## Licensing
- Loot tables you generate with text you own are yours to use freely.
- Public domain books are sourced from [Project Gutenberg](https://www.gutenberg.org/).
- Babel tool and data pack are copyright Joseph Fowler. A credit is appreciated but not required.

## Disclaimer
Software is provided "as is," without warranty or liability. Use at your own risk.
