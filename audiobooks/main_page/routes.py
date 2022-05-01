"""Routes for main page module."""

from flask import Blueprint

import audiobooks

VERSION_STRING = f"{audiobooks.__package__.title()} v{audiobooks.__version__}"

main_blueprint = Blueprint("main", __name__, template_folder="templates")


@main_blueprint.route("/")
def hello() -> str:
    return f"<b>{VERSION_STRING}</b>"
