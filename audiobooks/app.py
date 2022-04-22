"""Base Flask web application."""

from flask import Flask

from audiobooks import __version__

VERSION_STRING = f"{__package__.title()} v.{__version__}"
app = Flask(__name__)


@app.route("/")
def hello():
    return f"<b>{VERSION_STRING}</b>"
