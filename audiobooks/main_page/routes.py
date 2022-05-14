"""Routes for main page module."""

from flask import Blueprint, Response, make_response

import audiobooks

main_blueprint = Blueprint("main", __name__, template_folder="templates")


@main_blueprint.route("/")
def hello() -> Response:
    """A simple welcome message.

    Returns:
        Response: The message.
    """
    return make_response(
        f"<b>{audiobooks.__name__.title()}</b><p>{audiobooks.__version__}"
    )
