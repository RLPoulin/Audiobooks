"""Base database module."""

from __future__ import annotations

from typing import Any, TypeVar

from audiobooks.extensions import db

ModelType = TypeVar("ModelType", bound="Model")


class Model(db.Model):
    """Database base model."""

    __abstract__ = True
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.record_id})"

    @classmethod
    def get_by_id(cls: type[ModelType], record_id: int) -> ModelType | None:
        """Get a record by id.

        Args:
            record_id (int): The id of the record.

        Returns:
            ModelType | None: The record or None if not found.
        """
        return cls.query.get(record_id)

    @classmethod
    def get(cls: type[ModelType], record: ModelType | int) -> ModelType | None:
        """Get a record by itself or by id.

        Args:
            record (ModelType | int): The record or its id.

        Returns:
            ModelType | None: The record or None if not found.
        """
        return record if isinstance(record, Model) else cls.get_by_id(record)

    @classmethod
    def create(cls: type[ModelType], **kwargs) -> ModelType:
        """Create a new record and save it to the database.

        Args:
            kwargs: Keyword arguments to initialize the record.

        Returns:
            ModelType: The record.
        """
        return cls(**kwargs).save()

    def update(self, **kwargs) -> ModelType:
        """Update the columns of the record.

        Args:
            kwargs: {Column: value} pairs to update.

        Returns:
            ModelType: The record.
        """
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)
        return self.save()

    def save(self) -> ModelType:
        """Save the record to the database.

        Returns:
            ModelType: The record.
        """
        db.session.add(self)
        return self

    def delete(self) -> None:
        """Delete the record from the database."""
        db.session.delete(self)

    def to_dict(self) -> dict[str, Any]:
        """Convert the record to a dictionary.

        Returns:
            dict[str, Any]: Dictionary with the record columns as keys.
        """
        record_dict: dict[str, Any] = {}
        for column in db.inspect(self).mapper.column_attrs:
            column_name = column.key
            value = getattr(self, column_name)
            if hasattr(value, "to_dict"):
                value = value.to_dict()
            record_dict[column_name] = value
        return record_dict
