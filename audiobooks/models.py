"""Database table models for the audiobook library."""

from datetime import date
from typing import Dict, Optional, Type

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import RelationshipProperty, relationship

Base = declarative_base()


class ModelUnique(object):
    """Base class for a model containing only uniquely named items."""

    key: Column = Column(Integer, primary_key=True, autoincrement=True)
    _name: Column = Column("name", String, unique=True, nullable=False)

    def __init__(self, name: str, **kwargs) -> None:
        """Construct a model."""
        self.name: str = name

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}('{self.name}')>"

    def __str__(self) -> str:
        return self.name

    @hybrid_property
    def name(self) -> str:
        """Return the name property."""
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:  # noqa: WPS440
        """Set the name property."""
        self._name: str = clean_name(name=new_name)


class Author(ModelUnique, Base):
    """Defines the model for the ``authors`` table in the database."""

    __tablename__ = "authors"


class Series(ModelUnique, Base):
    """Defines the model for the ``series`` table in the database."""

    __tablename__ = "series"


class Genre(ModelUnique, Base):
    """Defines the model for the ``genres`` table in the database."""

    __tablename__ = "genres"


class Book(ModelUnique, Base):
    """Model for the for the ``books`` table in the database."""

    __tablename__ = "books"
    author_key: Column = Column(Integer, ForeignKey("authors.key"), nullable=False)
    genre_key: Column = Column(Integer, ForeignKey("genres.key"), nullable=False)
    series_key: Column = Column(Integer, ForeignKey("series.key"))
    release_date: Column = Column(Date)
    date_added: Column = Column(Date)

    author: RelationshipProperty = relationship("Author", backref=__tablename__)
    genre: RelationshipProperty = relationship("Genre", backref=__tablename__)
    series: RelationshipProperty = relationship("Series", backref=__tablename__)

    def __init__(self, name: str, author: Author, genre: Genre, **kwargs) -> None:
        """Construct a Book instance."""
        super().__init__(name)
        self.author: Author = author
        self.genre: Genre = genre
        self.series: Optional[Series] = kwargs.get("series", None)
        self.release_date: Optional[date] = kwargs.get("release_date", None)
        self.date_added: date = date.today()

    def __repr__(self) -> str:
        return f"<Book('{self.name}', author='{self.author}', genre='{self.genre}')>"  # noqa: WPS221,WPS221


# Dictionary associating book properties with the correct model.
MODELS: Dict[str, Type[ModelUnique]] = {
    "author": Author,
    "genre": Genre,
    "series": Series,
}


def clean_name(name: str) -> str:
    """Clean a string by capitalizing and removing extra spaces."""
    return " ".join(name.strip().split()).title()
