"""Database interactions for the audiobook library."""

__version__ = "0.3.0"
__all__ = ["CachedSession", "LibraryDatabase"]

from contextlib import contextmanager
from typing import Any, ContextManager, Dict, List, Optional, Tuple, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from audiobooks.log import log_manager
from audiobooks.models import Base, MODELS, ModelUnique, clean_name


log = log_manager.setup_logger(__name__)


class CachedSession(Session):
    """Database session with added instance cache."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize a cached session instance."""
        super().__init__(*args, **kwargs)
        self.cache: Dict[Tuple[Type[ModelUnique], str], ModelUnique] = {}

    def get(self, model: Type[ModelUnique], name: str) -> ModelUnique:
        """Get the instance with a name and a model from the cache or database."""
        name = clean_name(name=name)
        if (model, name) in self.cache:
            instance: ModelUnique = self.cache[(model, name)]
            log.debug(f"Got from cache: {instance!r}")
        else:
            instance: ModelUnique = self.query(model).filter(model.name == name).first()
            if instance:
                self.cache[(model, name)] = instance
                log.debug(f"Got from database: {instance!r}")
            else:
                log.debug(f"Failed to get: <{model.__name__}('{name}')>")
        return instance

    def create(self, model: Type[ModelUnique], name: str, **kwargs: Any) -> ModelUnique:
        """Create a model instance or get it if it already exists."""
        name = clean_name(name)
        instance: ModelUnique = self.get(name=name, model=model)
        if instance:
            return instance
        for key, argument in kwargs.items():
            if key in MODELS and isinstance(argument, str):
                kwargs[key] = self.create(name=argument, model=MODELS[key])
        instance: ModelUnique = model(name=name, **kwargs)
        self.add(instance)
        return instance

    def add(self, instance: ModelUnique, warn: Optional[bool] = True) -> None:
        """Add an instance to the database."""
        super().add(instance=instance, _warn=warn)
        self.cache[(instance.__class__, instance.name)] = instance
        log.info(f"Added: {instance!r}")

    def add_all(self, instances: List[ModelUnique]) -> None:
        """Add a list of instances to the database."""
        for instance in instances:
            self.add(instance)

    def delete(self, instance: ModelUnique) -> None:
        """Delete an instance from the database."""
        super().delete(instance)
        log.info(f"Deleted: {instance!r}")

    def commit(self) -> None:
        """Commit the current transaction to the database."""
        self.cache = {}
        super().commit()

    def rollback(self) -> None:
        """Rollback the current transaction."""
        self.cache = {}
        super().rollback()

    def get_index(self, model: Type[ModelUnique]) -> Dict[str, str]:
        """Return an index dictionary from a table in the database."""
        index = self.query(model).all()
        return {entry.key: entry.name for entry in index}


class LibraryDatabase:
    """Interface to interact with the database."""

    def __init__(self, filename: str) -> None:
        """Initialize the database."""
        self._filename: str = filename
        self._engine = create_engine(f"sqlite:///{filename}")
        self._session_maker: sessionmaker = sessionmaker(
            bind=self._engine, class_=CachedSession
        )
        Base.metadata.create_all(self._engine)
        log.info(f"Connected: {self!r}")

    def __repr__(self) -> str:
        return f"<LibraryDatabase('{self.filename}')>"

    def __str__(self) -> str:
        return self.filename

    @property
    def filename(self) -> str:
        return self._filename

    @contextmanager
    def session_scope(self) -> ContextManager:
        """Create a context manager for a database session."""
        session: CachedSession = self._session_maker()
        log.info("Database session started.")
        try:
            yield session
            session.commit()
        except Exception as exception:
            session.rollback()
            log.exception(
                f"Error while committing transaction: Rolling back changes:\n"
                f"{exception}"
            )
            raise
        finally:
            session.close()
            log.info("Database session closed.")

    def clear(self) -> None:
        """Clear the database."""
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        log.warning("Database cleared.")
