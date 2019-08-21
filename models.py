"""Database table models for the audiobook library."""

import typing as t
from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

__version__ = "0.1.0"

Base = declarative_base()


class ModelUnique:
    """Base class for a model containing only uniquely named items."""

    key = Column(Integer, primary_key=True, autoincrement=True)
    _name = Column("name", String, unique=True, nullable=False)

    def __init__(self, name: str, **kwargs: t.Any) -> None:
        """Construct a model."""
        self.name = name

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}('{self.name}')>"

    def __str__(self) -> str:
        return self.name

    @hybrid_property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value) -> None:
        self._name: str = self.clean_name(name=value)

    @staticmethod
    def clean_name(name: str) -> str:
        return " ".join(name.strip().split()).title()


class Author(ModelUnique, Base):
    """Defines the model for the ``authors`` table in the database."""

    __tablename__ = "authors"

    def __init__(self, name: str) -> None:
        """Construct an Author instance."""
        super().__init__(name)


class Series(ModelUnique, Base):
    """Defines the model for the ``series`` table in the database."""

    __tablename__ = "series"

    def __init__(self, name: str) -> None:
        """Construct a Series instance."""
        super().__init__(name)


class Genre(ModelUnique, Base):
    """Defines the model for the ``genres`` table in the database."""

    __tablename__ = "genres"

    def __init__(self, name: str) -> None:
        """Construct a Genre instance."""
        super().__init__(name)


class Book(ModelUnique, Base):
    """Model for the for the ``books`` table in the database."""

    __tablename__ = "books"
    author_key = Column(Integer, ForeignKey("authors.key"), nullable=False)
    genre_key = Column(Integer, ForeignKey("genres.key"), nullable=False)
    series_key = Column(Integer, ForeignKey("series.key"))
    release_date = Column(Date)
    date_added = Column(Date)

    author = relationship("Author", backref="books")
    genre = relationship("Genre", backref="books")
    series = relationship("Series", backref="books")

    def __init__(
        self,
        name: str,
        author: Author,
        genre: Genre,
        series: t.Optional[Series] = None,
        release_date: t.Optional[date] = None,
    ) -> None:
        """Construct a Book instance."""
        super().__init__(name)
        self.author = author
        self.genre = genre
        self.series = series
        self.release_date = release_date
        self.date_added: date = date.today()

    def __repr__(self) -> str:
        return f"<Book('{self.name}', author='{self.author}', genre='{self.genre}')>"


# Dictionary associating the Book properties with the correct model.
MODELS: t.Dict[str, t.Type[ModelUnique]] = {
    "author": Author,
    "genre": Genre,
    "series": Series,
}
