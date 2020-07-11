# Babel Book Loot
## A customisable pre-written book loot datapack for Minecraft

Babel Book Loot adds over 100 pre-written books to various loot tables in Minecraft. The default library of books is a collection of public domain fairy tales. You can customise the library by adding your own text files.

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
You can disable various book drops using command line options. Use `babel.py -h` to see the complete list. An example where zombie do not drop books:
```
babel.py -d zombie
````

You can add books to other loot tables using type `loot_table` and name `babel:books`.

### Dealing with datapack conflicts
If any of your other datapacks modify loot tables used by babel, it might be possible to create a compatible pack. To do this, replace the loot tables in `base_loot_tables` with the ones from the conflicting datapack.

### For use making your own datapacks
If you just want to generate the loot table without the surrounding files, try:
```
build_loottable.py > books.json
```

## Comments, suggestions or contributions?
Please use the Issue Tracker on GitHub, or send me a tweet @JiFish
