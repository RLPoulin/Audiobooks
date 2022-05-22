"""Base configuration for Flask application."""

import environs

environment = environs.Env()
environment.read_env()

LOG_LEVEL: str = environment.str("LOG_LEVEL", default="WARNING").upper()

ENV: str = environment.str("FLASK_ENV", default="production")
SECRET_KEY: str = environment.str("SECRET_KEY")

SQLALCHEMY_DATABASE_URI: str = f"sqlite:///{environment.path('DATABASE_URI').resolve()}"
SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

CACHE_TYPE: str = "simple"
CACHE_DEFAULT_TIMEOUT: int = 300
