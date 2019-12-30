"""Creates a database in an SQLite file and does some tests."""

__all__ = ["do_tests", "populate_database", "add_to_library"]

from datetime import date
from pathlib import Path
from typing import Dict

from audiobooks.database import LibraryDatabase
from audiobooks.log import log_manager
from audiobooks.models import Author, Book, Genre, Series

log = log_manager.setup_logger(__name__)


def do_tests() -> None:
    log_manager.set_default_levels(stream_level="DEBUG", setup_loggers=True)

    log.info("Testing adding entries to an empty database")
    populate_database(clear=True)

    log.info("Testing adding entries to an existing database")
    populate_database(clear=False)

    log.info("Done")
    log_manager.shutdown()


def populate_database(clear: bool = False) -> None:
    """Execute the program."""
    library: LibraryDatabase = LibraryDatabase(
        Path(__file__).parent.parent / "data" / "test.sqlite"
    )

    if clear:
        library.clear()

    books: Dict[str, str] = add_to_library(library)

    log_manager.flush_logger(log)
    print()
    print("End state list of books:")
    for book, name in books.items():
        print(f"{book:-4d}: {name}")
    print()


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
    do_tests()
