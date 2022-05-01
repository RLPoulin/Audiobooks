"""Base Flask web application."""

import flask

from audiobooks.extensions import cache, db, migrate
from audiobooks.library.routes import library_blueprint
from audiobooks.main_page.routes import main_blueprint


def create_app(config_object: str = "audiobooks.configuration") -> flask.Flask:
    app = flask.Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app: flask.Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)


def register_blueprints(app: flask.Flask) -> None:
    app.register_blueprint(main_blueprint)
    app.register_blueprint(library_blueprint)
