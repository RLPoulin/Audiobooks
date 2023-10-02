"""Tests for audiobooks.library.models."""

from decimal import Decimal

import flask_sqlalchemy
import pytest

from audiobooks.library.models import Author, Book, date, get_library_item


@pytest.fixture()
def author(test_db: flask_sqlalchemy.SQLAlchemy) -> Author:
    """Generate an Author example."""
    test_author = Author.create(name="Alice Bob")
    test_db.session.commit()
    return test_author


@pytest.fixture()
def book(test_db: flask_sqlalchemy.SQLAlchemy) -> Book:
    """Generate an Author example."""
    test_book = Book.create(name="Example", author="Alice Bob", series_number="1.1")
    test_db.session.commit()
    return test_book


def test_author_repr(author: Author) -> None:
    """Test for Author.__repr__ method."""
    assert f"{author!r}" == "Author('Alice Bob')"


def test_author_date_added(author: Author) -> None:
    """Test for Author.date_added column."""
    db_item = Author.get_by_id(author.record_id)
    assert db_item is not None
    assert db_item.date_added == date.today()


def test_author_get_by_name(author: Author) -> None:
    """Test for Author.get_by_name method."""
    assert Author.get_by_name("Alice Bob") is author


def test_author_get_by_name__dirty(author: Author) -> None:
    """Test for Author.get_by_name method using a dirty name."""
    assert Author.get_by_name("  ALICE  bOb") is author


def test_author_get_by_name__failure(author: Author) -> None:
    """Test for Author.get_by_name method returns None if it can't find the name."""
    assert Author.get_by_name("FAIL") is None


def test_author_get(author: Author) -> None:
    """Test for Author.get method with an Author as input."""
    assert Author.get(author) is author


def test_author_books(author: Author, book: Book) -> None:
    """Test for Author.books Book.author relationship."""
    db_book = Book.get_by_id(book.record_id)
    assert db_book is not None
    assert db_book.author is author
    db_author = Author.get_by_id(author.record_id)
    assert db_author is not None
    assert db_author.books == [book]


def test_book_create__default(test_db: flask_sqlalchemy.SQLAlchemy) -> None:
    """Test for Book.create method with default arguments."""
    book = Book.create(name="Example")
    test_db.session.commit()
    db_book = Book.get_by_id(book.record_id)
    assert db_book is not None
    assert db_book.record_id == 1
    assert db_book.name == "Example"
    assert db_book.author is None
    assert db_book.genre is None
    assert db_book.series is None
    assert db_book.date_added == date.today()
    assert db_book.series_number is None
    assert db_book.release_date is None


def test_book_create__from_objects(
    author: Author, test_db: flask_sqlalchemy.SQLAlchemy
) -> None:
    """Test for Book.create method with object arguments."""
    book = Book.create(
        name="Example",
        author=author,
        series_number=Decimal("1.1"),
        release_date=date(2020, 10, 10),
    )
    test_db.session.commit()
    db_book = Book.get_by_id(book.record_id)
    assert db_book is not None
    assert db_book.author is author
    assert db_book.series_number == Decimal("1.1")
    assert db_book.release_date == date(2020, 10, 10)


def test_book_create__from_strings(
    author: Author, test_db: flask_sqlalchemy.SQLAlchemy
) -> None:
    """Test for Book.create method with string arguments."""
    book = Book.create(
        name="Example",
        author="Alice Bob",
        series_number="1.1",
        release_date="2020-10-10",
    )
    test_db.session.commit()
    db_book = Book.get_by_id(book.record_id)
    assert db_book is not None
    assert db_book.author is author
    assert db_book.series_number == Decimal("1.1")
    assert db_book.release_date == date(2020, 10, 10)


def test_get_library_item() -> None:
    """Test for the get_library_item function."""
    assert get_library_item("author") == Author
    assert get_library_item("FAIL") is None


def test_to_dict(author: Author, book: Book) -> None:
    """Test for Model.to_dict method."""
    db_author = Author.get_by_id(author.record_id)
    assert db_author is not None
    assert db_author.to_dict() == {
        "model": "Author",
        "record_id": 1,
        "books": ["Example"],
        "date_added": date.today().isoformat(),
        "name": "Alice Bob",
    }
    db_book = Book.get_by_id(book.record_id)
    assert db_book is not None
    assert db_book.to_dict() == {
        "model": "Book",
        "record_id": 1,
        "author": "Alice Bob",
        "date_added": date.today().isoformat(),
        "genre": None,
        "name": "Example",
        "release_date": None,
        "series": None,
        "series_number": "1.1",
    }
