"""Defines fixtures for all tests."""

import os

import flask
import flask_sqlalchemy
import pytest

from audiobooks.app import create_app
from audiobooks.database import db


os.environ["LOG_LEVEL"] = "CRITICAL"


@pytest.fixture
def app() -> flask.Flask:
    """Create an application for the tests."""
    test_app: flask.Flask = create_app("tests.configuration.TestConfig")
    test_app.logger.setLevel("CRITICAL")
    test_context = test_app.test_request_context()
    test_context.push()

    yield test_app
    test_context.pop()


@pytest.fixture
def _db(app: flask.Flask) -> flask_sqlalchemy.SQLAlchemy:
    """Create a database for the tests."""
    db.app = app
    with app.app_context():
        db.create_all()

    yield db
    db.session.close()
    db.drop_all()
