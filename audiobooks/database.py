"""Database interactions for the audiobook library."""

from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from audiobooks.log import log_manager
from audiobooks.models import MODELS, Base, ModelType, ModelUnique, clean_name

log = log_manager.get_logger(__name__)


class CachedSession(Session):
    """Database session with added instance cache."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize a cached session instance."""
        super().__init__(*args, **kwargs)
        self.cache: dict[tuple[ModelType, str], ModelUnique] = {}

    def get_instance(self, model: ModelType, name: str) -> ModelUnique | None:
        """Get an instance object from the cache or database.

        Args:
            model: type of the instance
            name: name of the instance

        Returns:
            ModelUnique: the instance object, or None if it wasn't found
        """
        name = clean_name(name=name)
        instance: ModelUnique | None = self.cache.get((model, name), None)
        if instance:
            log.debug("Got from cache: %s", repr(instance))
            return instance
        instance: ModelUnique | None = (
            self.query(model).filter(model.name == name).first()
        )
        if instance:
            self.cache[(model, name)] = instance
            log.debug("Got from database: %s", repr(instance))
            return instance
        log.debug("Failed to get: <%s('%s')>", model.__name__, name)
        return None

    def create(self, model: ModelType, name: str, **kwargs: Any) -> ModelUnique:
        """Create a new model instance, or get it from the database if it already exists.

        Args:
            model: type of the instance
            name: name of the instance
            kwargs: additional model information for the creation of the instance

        Returns:
            ModelUnique: the created instance object
        """
        name = clean_name(name)
        instance: ModelUnique | None = self.get_instance(name=name, model=model)
        if instance:
            return instance
        for key, argument in kwargs.items():
            if key in MODELS and isinstance(argument, str):
                kwargs[key] = self.create(name=argument, model=MODELS[key])
        instance: ModelUnique = model(name=name, **kwargs)
        self.add(instance)
        return instance

    def add(self, instance: ModelUnique, warn: bool = True) -> None:
        """Add an instance to the database.

        Args:
            instance: the instance object to add to the database
            warn: display warnings
        """
        super().add(instance=instance, _warn=warn)
        self.cache[(instance.__class__, instance.name)] = instance
        log.debug("Added: %s", repr(instance))

    def delete(self, instance: ModelUnique) -> None:
        """Delete an instance from the database.

        Args:
            instance: the instance object to delete from the database
        """
        super().delete(instance)
        log.info("Deleted: %s", repr(instance))

    def commit(self) -> None:
        """Commit the current transaction to the database."""
        super().commit()
        self.cache = {}

    def rollback(self) -> None:
        """Rollback the current transaction."""
        super().rollback()
        self.cache = {}

    def get_index(self, model: ModelType) -> dict[str, str]:
        """Return an index from a table in the database.

        Args:
            model: type of the table to query

        Returns:
            dict[str, str]: index as a {'key number': 'name'} dictionary
        """
        index = self.query(model).all()
        return {str(entry.key): str(entry.name) for entry in index}


class LibraryDatabase:
    """Interface to interact with the database."""

    def __init__(self, file_path: Path | str) -> None:
        """Initialize the database.

        Args:
            file_path: path to the database file
        """
        self._file_path: Path = Path(file_path).resolve()
        self._engine = create_engine(f"sqlite:///{str(file_path)}")
        self._session_maker: sessionmaker = sessionmaker(
            bind=self._engine, class_=CachedSession
        )
        Base.metadata.create_all(self._engine)
        log.info("Connected: %s", repr(self))

    def __repr__(self) -> str:
        return f"<LibraryDatabase('{self.file_path}')>"

    def __str__(self) -> str:
        return str(self.file_path)

    @property
    def file_path(self) -> Path:
        """Return the file_path property."""
        return self._file_path

    @contextmanager
    def session_scope(self) -> Generator[CachedSession, None, None]:
        """Create a context manager for a database session."""
        session: CachedSession = self._session_maker()
        log.debug("Database session started.")
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            log.error("Exception while committing transaction, rolling back changes.")
            raise
        finally:
            session.close()
            log.debug("Database session closed.")

    def clear(self) -> None:
        """Clear the database."""
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        log.warning("Database cleared.")
