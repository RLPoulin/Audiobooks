"""Tests for audiobooks.library.models."""
from decimal import Decimal

import flask_sqlalchemy
import pytest

from audiobooks.library.models import Author, Book, date, get_library_item


@pytest.fixture
def author(test_db: flask_sqlalchemy.SQLAlchemy) -> Author:
    """Generate an Author example."""
    new_author = Author.create(name="Alice Bob")
    test_db.session.commit()
    return new_author


@pytest.fixture
def book(test_db: flask_sqlalchemy.SQLAlchemy) -> Book:
    """Generate an Author example."""
    new_book = Book.create(name="Book", author="Alice Bob")
    test_db.session.commit()
    return new_book


def test_author_repr(author: Author) -> None:
    """Test for Author.__repr__ method."""
    assert f"{author!r}" == "Author('Alice Bob')"


def test_author_date_added(author: Author) -> None:
    """Test for Author.date_added column."""
    assert Author.get_by_id(author.record_id).date_added == date.today()


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
    """Test for Author.books column."""
    assert Book.get_by_id(book.record_id).author is author
    assert Author.get_by_id(author.record_id).books == [book]


def test_book_create__default(test_db: flask_sqlalchemy.SQLAlchemy) -> None:
    """Test for Book.create method with default arguments."""
    book = Book.create(name="Book")
    test_db.session.commit()
    assert Book.get_by_id(book.record_id).record_id == 1
    assert Book.get_by_id(book.record_id).name == "Book"
    assert Book.get_by_id(book.record_id).date_added == date.today()
    assert Book.get_by_id(book.record_id).author is None


def test_book_create__object(
    author: Author, test_db: flask_sqlalchemy.SQLAlchemy
) -> None:
    """Test for Book.create method with object arguments."""
    book = Book.create(
        name="Book",
        author=author,
        series_number=Decimal("1.1"),
        release_date=date(2020, 10, 10),
    )
    test_db.session.commit()
    assert Book.get_by_id(book.record_id).author is author
    assert Book.get_by_id(book.record_id).series_number == Decimal("1.1")
    assert Book.get_by_id(book.record_id).release_date == date(2020, 10, 10)


def test_book_create__string(
    author: Author, test_db: flask_sqlalchemy.SQLAlchemy
) -> None:
    """Test for Book.create method with string arguments."""
    book = Book.create(
        name="Book",
        author="Alice Bob",
        series_number="1.1",
        release_date="2020-10-10",
    )
    test_db.session.commit()
    assert Book.get_by_id(book.record_id).author is author
    assert Book.get_by_id(book.record_id).series_number == Decimal("1.1")
    assert Book.get_by_id(book.record_id).release_date == date(2020, 10, 10)


def test_get_library_item() -> None:
    """Test for the get_library_item function."""
    assert get_library_item("author") == Author
    assert get_library_item("FAIL") is None
