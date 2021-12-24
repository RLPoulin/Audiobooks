"""Database table models for the audiobook library."""

from datetime import date
from types import MappingProxyType
from typing import TYPE_CHECKING, Type

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from titlecase import titlecase

if TYPE_CHECKING:
    hybrid_property = property
else:
    from sqlalchemy.ext.hybrid import hybrid_property


Base = declarative_base()


class ModelUnique:
    """Base class for a model containing only uniquely named items."""

    key = Column(Integer, primary_key=True, autoincrement=True)
    _name = Column("name", String, unique=True, nullable=False)

    def __init__(self, name: str, **kwargs) -> None:
        """Construct a model instance.

        Args:
            name: name of the instance
            kwargs: additional instance fields
        """
        self.name: str = name

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}('{self.name}')>"  # noqa

    def __str__(self) -> str:
        return self.name  # noqa

    @hybrid_property
    def name(self) -> str:
        """Return the name property."""
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        """Set the name property."""
        self._name = clean_name(name=new_name)


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
    """Model for the ``books`` table in the database."""

    __tablename__ = "books"
    author_key = Column(Integer, ForeignKey("authors.key"), nullable=False)
    genre_key = Column(Integer, ForeignKey("genres.key"))
    series_key = Column(Integer, ForeignKey("series.key"))
    release_date = Column(Date)
    date_added = Column(Date)

    author = relationship("Author", backref=__tablename__)
    genre = relationship("Genre", backref=__tablename__)
    series = relationship("Series", backref=__tablename__)

    def __init__(
        self,
        name: str,
        author: Author,
        *,
        genre: Genre | None = None,
        series: Series | None = None,
        release_date: date | None = None,
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
        self.date_added = date.today()

    def __repr__(self) -> str:
        return f"<Book('{self.name}', author='{self.author}')>"  # noqa


# Dictionary associating book properties with the correct model.
ModelType = Type[ModelUnique]
MODELS: MappingProxyType[str, ModelType] = MappingProxyType(
    {"author": Author, "genre": Genre, "series": Series}
)


def clean_name(name: str) -> str:
    """Clean a string by capitalizing and removing extra spaces.

    Args:
        name: the name to be cleaned

    Returns:
        str: the cleaned name
    """
    name = " ".join(name.strip().split())
    return str(titlecase(name))
