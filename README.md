# Babel Book Loot v0.5
## A customisable pre-written book loot datapack for Minecraft

Babel Book Loot adds over 100 pre-written books to various loot tables in Minecraft. The default library of books is a collection of public domain fairy tales. You can customise the library by adding your own text files.

It was last updated for Minecraft 1.18.2, but it should work in a wide range of versions.

## Quick-start
Run `babel.py`. It will generate babel.zip. Put that file in your Minecraft world's datapack directory.

Run `babel.py -h` to see more options.

## How the datapack works in-game
Written books can be dropped by zombies if killed by a player, or fished up with a fishing rod. They can also be found in villages, stronghold libraries and woodland mansions in chests.

The generation of the book is determined randomly
- 69% Tattered Book
- 30% Copy of a copy
- 1% Copy of original
- <1% Original

## Customising Books
Any books in the `books` directory will be included. You can add and remove books as you wish.

To create your own books go to https://minecraft.tools/en/book.php Once you've finished copy the command and delete the text `/give @p written_book` from the start. Then save it in `books` as `<Your Title>.json`.

### Submitting books
If you've made some books and the text is in the public domain, please consider submitting them back here!

### Default library
The default collection of books was sourced from Project Gutenberg. https://www.gutenberg.org/

## Advanced Customisation
### Altering where books will be found
You can disable various book drops using command line options. Use `babel.py -h` to see the complete list. An example where zombies do not drop books:
```
babel.py -d zombie
````

You can add books to other loot tables using type `loot_table` and name `babel:books`.

### Dealing with datapack conflicts
If any of your other datapacks modify loot tables used by babel, it might be possible to create a compatible pack. To do this, replace the loot tables in the `base_loot_tables` with the ones from the conflicting datapack. This isn't guaranteed to work, and won't if the tables are much different from expected.

### For use making your own datapacks
If you just want to generate the loot table without the surrounding files, try:
```
build_loottable.py > books.json
```

### Advanced Customising Books
If you build your own datapacks, you have probably noticed the format of books the `books` directory is JSON. Minecraft accepts strictly non-valid JSON, so babel tries to too. Babel does it's best to read the books, but if it's having issues your best bet is to ensure the file is valid JSON.

The JSON determines the NBT tags to be added to the Written Book item. See the [full specification](https://minecraft.fandom.com/wiki/Player.dat_format#Written_Books) for more information. You could even add other tags such as `CustomModelData`.

Bonus tip: Babel actually uses a YAML parser to read the books, so you can format your books as YAML if you wish.

## Comments, suggestions or contributions?
Please use the Issue Tracker on GitHub, or send me a tweet [@JiFish](https://twitter.com/intent/tweet?text=.@JiFish)

## Copyright & use in your own datapacks
Assuming the books are your own work, loot tables outputted by babel belong to you. You can use them freely in your own datapack. A credit is apprecicated, but not required.

Books in the `books` directory are in the public domain. The loot table created from them is also in the public domain.

The babel tool and datapack is copyright Joseph Fowler.

Disclaimer: Software provided is "as is", without a warranty, and should be used at your own risk.
