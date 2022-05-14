"""Base database module."""

from typing import Any, SupportsInt, TypeVar

from audiobooks.extensions import db

ModelType = TypeVar("ModelType", bound="Model")


class Model(db.Model):
    """Database base model."""

    __abstract__ = True
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.record_id})"

    @classmethod
    def get_by_id(
        cls: type[ModelType], record_id: SupportsInt | str
    ) -> ModelType | None:
        """Get a record by id."""
        try:
            record_id = int(record_id)
        except ValueError:
            return None
        return cls.query.get(record_id)

    @classmethod
    def create(cls: type[ModelType], **kwargs) -> ModelType:
        """Create a new record and save it to the database."""
        return cls(**kwargs).save()

    def update(self, **kwargs) -> ModelType:
        """Update the record."""
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)
        return self.save()

    def save(self) -> ModelType:
        """Save the record to the database."""
        db.session.add(self)
        return self

    def delete(self) -> None:
        """Delete the record from the database."""
        db.session.delete(self)

    def to_dict(self) -> dict[str, Any]:
        """Convert the record to a dictionary."""
        record_dict: dict[str, Any] = {}
        for column in db.inspect(self).mapper.column_attrs:
            column_name = column.key
            value = getattr(self, column_name)
            if hasattr(value, "to_dict"):
                value = value.to_dict()
            record_dict[column_name] = value
        return record_dict
