"""Creates a database in an SQLite file and does some tests."""

__version__ = "0.2.1"

from datetime import date
from typing import Dict

from database import LibraryDatabase, log_manager
from models import Author, Book, Genre, Series

log = log_manager.setup_logger(__name__)


def main(clear: bool = False) -> None:
    """Execute the program."""
    library: LibraryDatabase = LibraryDatabase("test.sqlite")
    if clear:
        library.clear()

    books: Dict[str, str] = add_to_library(library)

    log_manager.flush_logger(log)
    print("\nEnd state list of books:")
    for book, name in books.items():
        print(f"{book:-4d}: {name}")


def add_to_library(library: LibraryDatabase) -> Dict[str, str]:
    """Add test entries into the database."""
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
            model=Book,
            name="The Fault in our Stars",
            author="John Green",
            genre="Contemporary",
        )
        return session.get_index(Book)


if __name__ == "__main__":
    main(clear=True)
    main(clear=False)
    log_manager.shutdown()
