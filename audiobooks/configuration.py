"""Base configuration for Flask application."""

import environs

environment = environs.Env()
environment.read_env()

ENV = environment.str("FLASK_ENV", default="production")
SECRET_KEY = environment.str("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = f"sqlite:///{environment.path('DATABASE_URI').resolve()}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

CACHE_TYPE = "simple"
CACHE_DEFAULT_TIMEOUT = 300
