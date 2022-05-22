"""Base configuration for Flask application."""

import environs

environment = environs.Env()
environment.read_env()

ENV: str = "development"
SECRET_KEY: str = "not-so-secret-in-tests"
TESTING: bool = True

SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

CACHE_TYPE: str = "simple"
CACHE_DEFAULT_TIMEOUT: int = 300
