"""Database table models for the audiobook library."""

import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from audiobooks.extensions import db

from .utils import clean_name


class LibraryModel(db.Model):
    """Base class for a model containing only uniquely named items."""

    __abstract__ = True
    key = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _name = db.Column("name", db.String, unique=True, nullable=False)

    def __init__(self, name: str, **kwargs) -> None:
        """Construct a model instance.

        Args:
            name: name of the instance
            kwargs: additional instance fields
        """
        self.name: str = name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.name}')"

    def __str__(self) -> str:
        return self.name

    @hybrid_property
    def name(self) -> str:
        """Return the name property."""
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        """Set the name property."""
        self._name = clean_name(name=new_name)


class Author(LibraryModel):
    """Defines the model for the ``authors`` table in the database."""

    __tablename__ = "authors"


class Series(LibraryModel):
    """Defines the model for the ``series`` table in the database."""

    __tablename__ = "series"


class Genre(LibraryModel):
    """Defines the model for the ``genres`` table in the database."""

    __tablename__ = "genres"


class Book(LibraryModel):
    """Model for the ``books`` table in the database."""

    __tablename__ = "books"
    author_key = db.Column(db.Integer, db.ForeignKey("authors.key"), nullable=False)
    genre_key = db.Column(db.Integer, db.ForeignKey("genres.key"))
    series_key = db.Column(db.Integer, db.ForeignKey("series.key"))
    release_date = db.Column(db.Date)
    date_added = db.Column(db.Date)

    author = db.relationship("Author", backref=__tablename__)
    genre = db.relationship("Genre", backref=__tablename__)
    series = db.relationship("Series", backref=__tablename__)

    def __init__(
        self,
        name: str,
        author: Author,
        *,
        genre: Genre | None = None,
        series: Series | None = None,
        release_date: datetime.date | None = None,
    ) -> None:
        """Construct a Book instance.

        Args:
            name: name of the book
            author: instance object for the author
            genre: instance object for the genre (optional)
            series: instance object for the series (optional)
            release_date: book release date (optional)
        """
        super().__init__(name)
        self.author = author
        self.genre = genre
        self.series = series
        self.release_date = release_date
        self.date_added = datetime.date.today()

    def __repr__(self) -> str:
        return f"<Book('{self.name}', author='{self.author}')>"  # noqa


# Dictionary associating book properties with the correct model.
LIBRARY_MODELS: dict[str, type[LibraryModel]] = {
    "author": Author,
    "book": Book,
    "genre": Genre,
    "series": Series,
}
