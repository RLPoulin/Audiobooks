"""Database table models for the audiobook library."""

import datetime
from typing import TypeVar

from sqlalchemy.ext.hybrid import hybrid_property

from audiobooks.database import Model
from audiobooks.extensions import db

from .utils import clean_name

LibraryModelType = TypeVar("LibraryModelType", bound="LibraryModel")


class LibraryModel(Model):
    """Base class for a model containing only uniquely named items."""

    __abstract__ = True
    _name = db.Column("name", db.String, unique=True, nullable=False)
    date_added = db.Column(db.Date, default=datetime.date.today)

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__()
        self.name = name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.name}')"

    @classmethod
    def get_by_name(cls, name: str) -> LibraryModelType:
        """Get a record by name."""
        return cls.query.filter_by(name=clean_name(name)).first()

    @hybrid_property
    def name(self) -> str:
        """Return the name property."""
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        """Set the name property."""
        self._name = clean_name(name=new_name)


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
    release_date = db.Column(db.Date)

    def __init__(
        self,
        name: str,
        *,
        author: Author | str | None = None,
        genre: Genre | str | None = None,
        series: Series | str | None = None,
        release_date: datetime.date | str | None = None,
    ) -> None:
        super().__init__(name)
        if isinstance(author, str):
            author = Author.get_by_name(author)
        if isinstance(genre, str):
            author = Genre.get_by_name(genre)
        if isinstance(series, str):
            author = Series.get_by_name(series)
        if isinstance(release_date, str):
            release_date = datetime.date.fromisoformat(release_date)
        self.author = author
        self.genre = genre
        self.series = series
        self.release_date = release_date


# Dictionary associating book properties with the correct model.
LIBRARY_MODELS: dict[str, type[LibraryModel]] = {
    "author": Author,
    "book": Book,
    "genre": Genre,
    "series": Series,
}
