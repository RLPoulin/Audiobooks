"""Base database module."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any, Self, get_args

import sqlalchemy.types

from audiobooks.extensions import db


SimpleType = int | str | None
SupportDecimal = Decimal | int | float | str


class Model(db.Model):
    """Database base model."""

    __abstract__ = True
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.record_id})"

    @classmethod
    def get_by_id(cls: type[Self], record_id: int | None) -> Self | None:
        """Get a record by id.

        Args:
            record_id (int): The id of the record.

        Returns:
            Model | None: The record or None if not found.
        """
        return cls.query.get(record_id) if record_id is not None else None

    @classmethod
    def get(cls: type[Self], record: Self | int | None) -> Self | None:
        """Get a record by itself or by id.

        Args:
            record (Model | int): The record or its id.

        Returns:
            Model | None: The record or None if not found.
        """
        return record if isinstance(record, Model) else cls.get_by_id(record)

    @classmethod
    def create(cls: type[Self], **kwargs) -> Self:
        """Create a new record and save it to the database.

        Args:
            kwargs: Keyword arguments to initialize the record.

        Returns:
            Model: The record.
        """
        return cls(**kwargs).save()

    def update(self, **kwargs) -> Self:
        """Update the columns of the record.

        Args:
            kwargs: {Column: value} pairs to update.

        Returns:
            Model: The record.

        Raises:
            KeyError: The column to be updated is not in the model.
        """
        for attribute, value in kwargs.items():
            if not hasattr(self, attribute):
                raise KeyError(f"{self!r} has no column '{attribute}'")
            setattr(self, attribute, value)
        return self.save()

    def save(self) -> Self:
        """Save the record to the database.

        Returns:
            Model: The record.
        """
        db.session.add(self)
        return self

    def delete(self) -> None:
        """Delete the record from the database."""
        db.session.delete(self)

    def to_dict(self) -> dict[str, SimpleType | list[SimpleType]]:
        """Creates a dictionary of the record.

        Returns:
            dict[str, SimpleType]: Dictionary with the record columns as keys.
        """
        descriptors: list[str] = db.inspect(self).mapper.all_orm_descriptors.keys()
        descriptors = sorted(
            d for d in descriptors if not d.startswith("_") and not d.endswith("_id")
        )
        record_dict: dict[str, SimpleType | list[SimpleType]] = {
            "model": type(self).__name__,
            "record_id": self.record_id,
        } | {d: _simplify_description(getattr(self, d)) for d in descriptors}
        return record_dict


class SqliteDecimal(sqlalchemy.types.TypeDecorator):
    """SQLAlchemy decimal type adapter for sqlite databases."""

    impl = sqlalchemy.types.Integer
    cache_ok = True

    def __init__(self, precision: int = 2) -> None:
        """Initialize an instance of SqliteDecimal.

        Args:
            precision (int, optional): Number of decimal places to store. Defaults to 2.
        """
        super().__init__()
        self.precision: int = precision
        self.multiplier: int = 10**self.precision

    def process_bind_param(
        self, value: SupportDecimal | None, dialect: sqlalchemy.engine.Dialect
    ) -> int | None:
        """Receive a bound parameter value to be converted."""
        return int(Decimal(value) * self.multiplier) if value is not None else None

    def process_result_value(
        self, value: SupportDecimal, dialect: sqlalchemy.engine.Dialect
    ) -> Decimal | None:
        """Receive a result-row column value to be converted."""
        return Decimal(value) / self.multiplier if value is not None else None


def _simplify_description(
    value: Any | list[Any],  # noqa: ANN401
) -> SimpleType | list[SimpleType]:
    if isinstance(value, list):
        return [_simplify_value(entry) for entry in value]
    return _simplify_value(value)


def _simplify_value(value: Any) -> SimpleType:  # noqa: ANN401
    if isinstance(value, get_args(SimpleType)):
        return value
    return value.isoformat() if isinstance(value, date) else str(value)
