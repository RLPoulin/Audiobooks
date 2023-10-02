"""Defines fixtures for all tests."""

import os

import flask
import flask_sqlalchemy
import pytest

from audiobooks.app import create_app
from audiobooks.configuration import Config
from audiobooks.database import db


os.environ["LOG_LEVEL"] = "CRITICAL"


class TestConfig(Config):
    """Configuration class for testing."""

    ENV: str = "development"
    SECRET_KEY: str = "no-secrets-in-tests"
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"


@pytest.fixture()
def app() -> flask.Flask:  # type: ignore[reportGeneralTypeIssue]
    """Create an application for the tests."""
    test_app: flask.Flask = create_app("tests.conftest.TestConfig")
    test_app.logger.setLevel("CRITICAL")
    test_context = test_app.test_request_context()
    test_context.push()

    yield test_app  # type: ignore[reportGeneralTypeIssue]
    test_context.pop()


@pytest.fixture()
def test_db(app: flask.Flask) -> flask_sqlalchemy.SQLAlchemy:  # type: ignore[reportGeneralTypeIssue]
    """Create a database for the tests."""
    db.app = app  # type: ignore[reportGeneralTypeIssue]
    with app.app_context():
        db.create_all()

    yield db  # type: ignore[reportGeneralTypeIssue]
    db.session.close()
    db.drop_all()
