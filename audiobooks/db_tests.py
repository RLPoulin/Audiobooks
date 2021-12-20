"""Creates a database in an SQLite file and does some tests."""

from datetime import date
from pathlib import Path

from audiobooks.database import LibraryDatabase
from audiobooks.log import flush_logger, logging
from audiobooks.models import Author, Book, Genre, Series

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logging.getLogger("audiobooks.database").setLevel(logging.DEBUG)
logging.getLogger("titlecase").setLevel(logging.WARNING)


def do_tests() -> None:
    """Start the db tests."""
    log.info("Testing adding entries to an empty database")
    test_database(clear=True)

    log.info("Testing adding entries to an existing database")
    test_database(clear=False)

    log.debug("Tests done")
    logging.shutdown()


def test_database(clear: bool = False) -> None:
    """Test the database and print content."""
    library_path: Path = Path(__file__).parent.parent / "data" / "test.sqlite"
    library_path.parent.mkdir(exist_ok=True)
    library: LibraryDatabase = LibraryDatabase(str(library_path))

    if clear:
        library.clear()

    books: dict[str, str] = add_to_library(library)

    flush_logger(log)
    log.info("End state list of books: %s", books)


def add_to_library(library: LibraryDatabase) -> dict[str, str]:
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
        sanderson = session.get(Author, "Brandon Sanderson")
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
