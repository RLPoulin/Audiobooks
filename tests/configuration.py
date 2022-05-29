"""Base configuration for Flask application."""

from audiobooks.configuration import Config


class TestConfig(Config):
    """Configuration class for testing."""

    ENV: str = "development"
    SECRET_KEY: str = "not-so-secret-in-tests"
    TESTING: bool = True

    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
