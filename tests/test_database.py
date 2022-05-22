"""Tests for audiobooks.database.Model."""

from __future__ import annotations

from decimal import Decimal

import flask_sqlalchemy

from audiobooks.database import Model, SqliteDecimal, SupportDecimal, db


class ModelExample(Model):
    """Example class implementing Model for testing."""

    name = db.Column(db.String)
    number = db.Column(SqliteDecimal)

    def __init__(self, name: str, number: SupportDecimal | None = None) -> None:
        """Initialize a new ModelExample instance."""
        super().__init__()
        self.name = name
        self.number = number


def test_repr(test_db: flask_sqlalchemy.SQLAlchemy) -> None:
    """Test for Model.__repr__ method."""
    example = ModelExample.create(name="name")
    test_db.session.commit()
    assert f"{example!r}" == "ModelExample(1)"


def test_get_by_id(test_db: flask_sqlalchemy.SQLAlchemy) -> None:
    """Test for Model.get_by_id method."""
    example = ModelExample.create(name="name")
    test_db.session.commit()
    assert ModelExample.get_by_id(example.record_id) is example


def test_get_by_id__failure() -> None:
    """Test that Model.get_by_id returns None if record_id doesn't exist."""
    assert ModelExample.get_by_id(999999) is None


def test_get(test_db: flask_sqlalchemy.SQLAlchemy) -> None:
    """Test for Model.get method."""
    example = ModelExample.create(name="name")
    test_db.session.commit()
    assert ModelExample.get(example) is example


def test_create(test_db: flask_sqlalchemy.SQLAlchemy) -> None:
    """Test for Model.create method."""
    example = ModelExample.create(name="name")
    test_db.session.commit()
    assert ModelExample.get_by_id(example.record_id).name == "name"


def test_update(test_db: flask_sqlalchemy.SQLAlchemy) -> None:
    """Test for Model.update method."""
    example = ModelExample.create(name="name")
    test_db.session.commit()
    example.update(name="new_name")
    test_db.session.commit()
    assert ModelExample.get_by_id(example.record_id).name == "new_name"


def test_delete(test_db: flask_sqlalchemy.SQLAlchemy) -> None:
    """Test for Model.delete method."""
    example = ModelExample.create(name="name")
    test_db.session.commit()
    example.delete()
    test_db.session.commit()
    assert ModelExample.get_by_id(example.record_id) is None


def test_to_dict(test_db: flask_sqlalchemy.SQLAlchemy) -> None:
    """Test for Model.to_dict method."""
    example = ModelExample.create(name="name")
    test_db.session.commit()
    example_dict = ModelExample.get_by_id(example.record_id).to_dict()
    assert example_dict == {"record_id": 1, "name": "name", "number": None}


def test_decimal(test_db: flask_sqlalchemy.SQLAlchemy) -> None:
    """Test for SqliteDecimal."""
    example = ModelExample.create(name="name", number=1.1)
    test_db.session.commit()
    assert ModelExample.get_by_id(example.record_id).number == Decimal("1.1")
    assert ModelExample.query.filter(ModelExample.number > 1).first() == example
    assert ModelExample.query.filter(ModelExample.number > 1.9).first() is None
