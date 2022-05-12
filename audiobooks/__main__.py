"""Flask app entry point."""

import logging

import flask
import rich.logging

from audiobooks.app import create_app
from audiobooks.configuration import environment
from audiobooks.extensions import db

logging.basicConfig(
    level=environment.str("LOG_LEVEL", default="WARNING").upper(),
    format="%(name)s: %(message)s",
    datefmt="%H:%M:%S",
    handlers=[rich.logging.RichHandler()],
)
logging.captureWarnings(capture=True)
logging.getLogger("werkzeug").handlers.clear()
logging.getLogger("titlecase").setLevel("WARNING")


def start_app() -> flask.Flask:
    app: flask.Flask = create_app()
    db.create_all(app=app)
    return app


def main() -> None:
    start_app().run()


if __name__ == "__main__":
    main()
