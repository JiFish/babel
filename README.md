# Babel Book Loot
## A customisable pre-written book loot datapack for Minecraft 1.14

Babel Book Loot adds 110 pre-written books to various loot tables in Minecraft. The default collection of books are public domain fairy tales.

### Quick-start
Run `babel`. It will generate babel.zip. Put that file in your minecraft worlds datapack directory.

Run `babel -h` to see more options.

### Customising Books
Any books in the `books` directory will be included. You can add and remove books as you wish.

The first line of the file is the author, the second the book title and after that each line is a page in the book. This does mean you have to size your pages correctly first. You can do this in minecraft itself.

If you need a line return on a page, you can use `\n`

#### Example book.txt
```
Author Name
Book Title
Page One.
Page Two.\nLine 2 on page 2.
```

#### Submiting books
If you've made some books and the text is in the public domain, please consider submitting them back here!

#### Default selection
The default selection of books was sourced from Project Gutenberg. https://www.gutenberg.org/

#### Support for JSON text / formatting?
Not at the moment. If enough people ask for it.
