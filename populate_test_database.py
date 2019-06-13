"""Creates a database in an SQLite file and does some tests."""

import typing as t
from datetime import date

import logger
from database import LibraryDatabase
from models import Author, Book, Genre, Series

__version__ = "0.1.1"

log = logger.get_logger(__name__, "info")


def main(clear: t.Optional[bool] = False) -> None:
    """Execute the program."""
    library: LibraryDatabase = LibraryDatabase("test.sqlite")

    if clear:
        library.clear()

    with library.session_scope() as session:
        session.create(model=Genre, name="Fantasy")
        session.create(
            model=Book,
            name="The Way of Kings",
            author="Brandon Sanderson",
            genre="Fantasy",
            series="The Stormlight Archive",
            release_date=date(2010, 8, 31),
        )
        sanderson: Author = session.get(Author, "Brandon Sanderson")
        session.create(
            model=Book,
            name="Words of Radiance",
            release_date=date(2014, 3, 4),
            author=sanderson,
            series="The Stormlight Archive",
            genre="Fantasy",
        )
        session.create(
            model=Book,
            name="Harry Potter and the Sorcerer's Stone",
            author="J.K. Rowling",
            series="Harry Potter",
            genre="Fantasy",
        )
        session.create(model=Series, name="The Expanse")
        session.create(
            model=Book, name="The Fault in our Stars", author="John Green", genre="Contemporary"
        )
        books = session.get_index(Book)

    logger.flush_logger(log)
    print("\nEnd state list of books:")
    for key, value in books.items():
        print(f"{key:-4d}: {value}")


if __name__ == "__main__":
    main(clear=True)
    main(clear=False)
    logger.close_logger()
