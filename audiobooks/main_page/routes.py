"""Routes for main page module."""

from flask import Blueprint

import audiobooks

main_blueprint = Blueprint("main", __name__, template_folder="templates")


@main_blueprint.route("/")
def hello() -> str:
    return f"<b>{audiobooks.__package__.title()}</b> v{audiobooks.__version__}"
