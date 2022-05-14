"""Flask app entry point."""

import logging

import rich.logging

from audiobooks.app import create_app
from audiobooks.configuration import environment

logging.basicConfig(
    level=environment.str("LOG_LEVEL", default="WARNING").upper(),
    format="%(name)s: %(message)s",
    datefmt="%H:%M:%S",
    handlers=[rich.logging.RichHandler()],
)
logging.captureWarnings(capture=True)
logging.getLogger("werkzeug").handlers.clear()
logging.getLogger("titlecase").setLevel("WARNING")


def main() -> None:
    create_app().run()


if __name__ == "__main__":
    main()
