"""Database table models for the audiobook library."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Any, Self

from sqlalchemy.ext.hybrid import hybrid_property

from audiobooks.database import Model, SqliteDecimal
from audiobooks.extensions import db

from .utils import clean_name


class LibraryModel(Model):
    """Base class for a model containing only uniquely named items."""

    __abstract__ = True
    _name = db.Column("name", db.String, unique=True, nullable=False)
    date_added = db.Column(db.Date, default=date.today)

    def __init__(self, name: str, **kwargs: dict[str, Any]) -> None:
        """Initialize a model record for an item in the library.

        Args:
            name (str): The name of the item.
            kwargs (Any): Additional arguments to be passed to the parent Model.
        """
        super().__init__(**kwargs)
        self.name = name

    def __str__(self) -> str:
        # noinspection PyPropertyAccess
        return self.name

    def __repr__(self) -> str:
        # noinspection PyPropertyAccess
        return f"{type(self).__name__}('{self.name}')"

    @classmethod
    def get_by_name(cls: type[Self], name: str) -> Self | None:
        """Get a record by name.

        Args:
            name (str): The name of the record.

        Returns:
            LibraryModel | None: The record or None if not found.
        """
        return cls.query.filter_by(name=clean_name(name)).first()

    @classmethod
    def get(cls: type[Self], record: Self | str | int) -> Self | None:
        """Get a record by itself, name, or id.

        Args:
            record (LibraryModel | str | int): The record, its name, or id.

        Returns:
            LibraryModel | None: The record or None if not found.
        """
        return (
            cls.get_by_name(record) if isinstance(record, str) else super().get(record)
        )

    @hybrid_property
    def name(self) -> str:
        """Return the name property."""
        return self._name

    @name.inplace.setter
    def _name_setter(self, value: str) -> None:
        """Set the name property."""
        self._name = clean_name(value)


class Author(LibraryModel):
    """Defines the model for the ``author`` table in the database."""

    books = db.relationship("Book", backref="author", lazy=True)


class Genre(LibraryModel):
    """Defines the model for the ``genre`` table in the database."""

    books = db.relationship("Book", backref="genre", lazy=True)


class Series(LibraryModel):
    """Defines the model for the ``series`` table in the database."""

    books = db.relationship("Book", backref="series", lazy=True)


class Book(LibraryModel):
    """Model for the ``book`` table in the database."""

    author_id = db.Column(db.Integer, db.ForeignKey("author.record_id"))
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.record_id"))
    series_id = db.Column(db.Integer, db.ForeignKey("series.record_id"))
    series_number = db.Column(SqliteDecimal(precision=3))
    release_date = db.Column(db.Date)

    def __init__(
        self,
        name: str,
        *,
        author: Author | str | None = None,
        genre: Genre | str | None = None,
        series: Series | str | None = None,
        series_number: Decimal | str | None = None,
        release_date: date | str | None = None,
    ) -> None:
        """Initialize a model record for a book.

        Args:
            name (str): The name of the book.
            author (Author | str | None, optional): The author of the book. Defaults to
                None.
            genre (Genre | str | None, optional): The genre of the book. Defaults to
                None.
            series (Series | str | None, optional): The series containing the book.
                Defaults to None.
            series_number (Decimal | None, optional): The book's order number in the
                series. Default to None.
            release_date (date | str | None, optional): The book's release date.
                Defaults to None.

        """
        super().__init__(name=name)
        self.author = Author.get(author) if author else None
        self.genre = Genre.get(genre) if genre else None
        self.series = Series.get(series) if series else None
        if isinstance(series_number, str):
            series_number = Decimal(series_number)
        self.series_number = series_number
        if isinstance(release_date, str):
            release_date = date.fromisoformat(release_date)
        self.release_date = release_date


class LibraryItems(Enum):
    """Enumeration of the different types of library items."""

    AUTHOR = Author
    BOOK = Book
    GENRE = Genre
    SERIES = Series


def get_library_item(item: str) -> type[LibraryModel] | None:
    """Gets the model class corresponding to the requested item type.

    Args:
        item (str): The name of the item.

    Returns:
        type[LibrayModel]: The model class.
    """
    try:
        return LibraryItems[item.upper()].value
    except KeyError:
        return None
