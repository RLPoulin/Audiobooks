"""Configuration for Flask application."""

from __future__ import annotations

from pathlib import Path

import environs


environment = environs.Env()
environment.read_env()

LOG_LEVEL: str = environment.str("LOG_LEVEL", default="WARNING").upper()

_database_env: str | None = environment.str("DATABASE_URI", default=None)
_database_path: Path | None = Path(_database_env).resolve() if _database_env else None


class Config:
    """Base configuration class."""

    ENV: str = environment.str("FLASK_ENV", default="production")
    SECRET_KEY: str | None = environment.str("SECRET_KEY", default=None)

    SQLALCHEMY_DATABASE_URI: str | None = (
        f"sqlite:///{_database_path}" if _database_path else None
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    CACHE_TYPE: str = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT: int = 300
