"""Database interactions for the audiobook library."""

import typing as t
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import logger
from models import Base, MODELS, ModelUnique

__version__ = "0.1.1"

log = logger.get_logger(__name__)


class CachedSession(Session):
    """Database session with added instance cache."""

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        """Constructs a cached session instance."""
        super().__init__(*args, **kwargs)
        self.cache: t.Dict[t.Tuple[t.Type[ModelUnique], str], ModelUnique] = {}

    def get(self, model: t.Type[ModelUnique], name: str) -> ModelUnique:
        """Get the instance with a name and a model from the cache or database."""
        name = model.clean_name(name=name)
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

    def create(
            self, model: t.Type[ModelUnique], name: str, **kwargs: t.Any
    ) -> ModelUnique:
        """Create a model instance or get it if it already exists."""
        name = model.clean_name(name)
        instance: ModelUnique = self.get(name=name, model=model)
        if instance:
            return instance
        for key, value in kwargs.items():
            if key in MODELS and isinstance(value, str):
                kwargs[key] = self.create(name=value, model=MODELS[key])
        instance: ModelUnique = model(name=name, **kwargs)
        self.add(instance)
        return instance

    def add(self, instance: ModelUnique, warn: t.Optional[bool] = True) -> None:
        """Add an instance to the database."""
        super().add(instance=instance, _warn=warn)
        self.cache[(instance.__class__, instance.name)] = instance
        log.info(f"Added: {instance!r}")

    def add_all(self, instances: t.List[ModelUnique]) -> None:
        """Add a list of instances to the database."""
        for item in instances:
            self.add(item)

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

    def get_index(self, model: t.Type[ModelUnique]) -> t.Dict[str, str]:
        """Return an index dictionary from a table in the database."""
        items = self.query(model).all()
        return {item.key: item.name for item in items}


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
    def session_scope(self) -> t.ContextManager:
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
