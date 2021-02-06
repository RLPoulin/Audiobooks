"""Database interactions for the audiobook library."""

from contextlib import contextmanager
from typing import Any, Generator, Optional, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from audiobooks.log import log_manager
from audiobooks.models import MODELS, Base, ModelUnique, clean_name

log = log_manager.setup_logger(__name__)
ModelType = Type[ModelUnique]


class CachedSession(Session):  # noqa: WPS214
    """Database session with added instance cache."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize a cached session instance."""
        super().__init__(*args, **kwargs)
        self.cache: dict[tuple[ModelType, str], ModelUnique] = {}

    def get(self, model: ModelType, name: str) -> Optional[ModelUnique]:
        """Get the instance with a name and a model from the cache or database."""
        name = clean_name(name=name)
        instance: Optional[ModelUnique] = self.cache.get((model, name), None)
        if instance:
            log.debug("Got from cache: %s", repr(instance))
            return instance
        instance: Optional[ModelUnique] = (
            self.query(model).filter(model.name == name).first()  # type: ignore
        )
        if instance:
            self.cache[(model, name)] = instance
            log.debug("Got from database: %s", repr(instance))
            return instance
        log.debug("Failed to get: <%s('%s')>", model.__name__, name)
        return None

    def create(self, model: ModelType, name: str, **kwargs: Any) -> ModelUnique:
        """Create a model instance or get it if it already exists."""
        name = clean_name(name)
        instance: Optional[ModelUnique] = self.get(name=name, model=model)
        if instance:
            return instance
        for key, argument in kwargs.items():
            if key in MODELS and isinstance(argument, str):
                kwargs[key] = self.create(name=argument, model=MODELS[key])
        instance: ModelUnique = model(name=name, **kwargs)
        self.add(instance)
        return instance

    def add(self, instance: ModelUnique, warn: bool = True) -> None:
        """Add an instance to the database."""
        super().add(instance=instance, _warn=warn)
        self.cache[(instance.__class__, instance.name)] = instance
        log.info("Added: %s", repr(instance))

    def delete(self, instance: ModelUnique) -> None:
        """Delete an instance from the database."""
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
        """Return an index dictionary from a table in the database."""
        index = self.query(model).all()
        return {str(entry.key): str(entry.name) for entry in index}


class LibraryDatabase(object):
    """Interface to interact with the database."""

    def __init__(self, filename: str) -> None:
        """Initialize the database."""
        self._filename: str = filename
        self._engine = create_engine(f"sqlite:///{filename}")
        self._session_maker: sessionmaker = sessionmaker(
            bind=self._engine, class_=CachedSession
        )
        Base.metadata.create_all(self._engine)
        log.info("Connected: %s", repr(self))

    def __repr__(self) -> str:
        return f"<LibraryDatabase('{self.filename}')>"

    def __str__(self) -> str:
        return self.filename

    @property
    def filename(self) -> str:
        """Return the filename property."""
        return self._filename

    @contextmanager
    def session_scope(self) -> Generator[CachedSession, None, None]:
        """Create a context manager for a database session."""
        session: CachedSession = self._session_maker()
        log.info("Database session started.")
        try:  # noqa: WPS229
            yield session
            session.commit()
        except Exception:
            session.rollback()
            log.exception("Error while committing transaction, rolling back changes.")
            raise
        finally:
            session.close()
            log.info("Database session closed.")

    def clear(self) -> None:
        """Clear the database."""
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        log.warning("Database cleared.")
