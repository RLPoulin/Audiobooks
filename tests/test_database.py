"""Tests for audiobooks.database.Model."""

from __future__ import annotations

from decimal import Decimal

import flask_sqlalchemy
import pytest

from audiobooks.database import Model, SqliteDecimal, SupportDecimal, db


class ExampleModel(Model):
    """Example class implementing Model for testing."""

    name = db.Column(db.String)
    number = db.Column(SqliteDecimal)

    def __init__(self, name: str, number: SupportDecimal | None = None) -> None:
        """Initialize a new ExampleModel instance."""
        super().__init__()
        self.name = name
        self.number: Decimal | None = Decimal(number) if number else None


@pytest.fixture()
def example(test_db: flask_sqlalchemy.SQLAlchemy) -> ExampleModel:
    """Generate a test example."""
    new_example = ExampleModel.create(name="name")
    test_db.session.commit()
    return new_example


def test_create() -> None:
    """Test for Model.create method."""
    item = ExampleModel.create(name="test")
    assert item.name == "test"


def test_repr(example: ExampleModel) -> None:
    """Test for Model.__repr__ method."""
    assert f"{example!r}" == "ExampleModel(1)"


def test_get_by_id(example: ExampleModel) -> None:
    """Test for Model.get_by_id method."""
    assert ExampleModel.get_by_id(example.record_id) is example


def test_get_by_id__not_exist() -> None:
    """Test that Model.get_by_id returns None if record_id doesn't exist."""
    assert ExampleModel.get_by_id(999999) is None


def test_get(example: ExampleModel) -> None:
    """Test for Model.get method."""
    assert ExampleModel.get(example) is example


def test_update(example: ExampleModel, test_db: flask_sqlalchemy.SQLAlchemy) -> None:
    """Test for Model.update method."""
    example.update(name="new_name")
    test_db.session.commit()
    db_item = ExampleModel.get_by_id(example.record_id)
    assert db_item is not None
    assert db_item.name == "new_name"


def test_delete(example: ExampleModel, test_db: flask_sqlalchemy.SQLAlchemy) -> None:
    """Test for Model.delete method."""
    example.delete()
    test_db.session.commit()
    assert ExampleModel.get_by_id(example.record_id) is None


def test_to_dict(example: ExampleModel) -> None:
    """Test for Model.to_dict method."""
    db_item = ExampleModel.get_by_id(example.record_id)
    assert db_item is not None
    example_dict = db_item.to_dict()
    assert example_dict == {
        "model": "ExampleModel",
        "record_id": 1,
        "name": "name",
        "number": None,
    }


def test_decimal(example: ExampleModel, test_db: flask_sqlalchemy.SQLAlchemy) -> None:
    """Test for SqliteDecimal."""
    example.update(number=1.1)
    test_db.session.commit()
    db_item = ExampleModel.get_by_id(example.record_id)
    assert db_item is not None
    assert db_item.number == Decimal("1.1")
    assert ExampleModel.query.filter(ExampleModel.number > 1).first() == example  # type: ignore[reportOptionalOperand]
    assert ExampleModel.query.filter(ExampleModel.number > 1.9).first() is None  # type: ignore[reportOptionalOperand]
