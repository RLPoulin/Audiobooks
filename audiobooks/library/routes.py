"""Routes for main page module."""

import logging

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from audiobooks.extensions import db

from .models import LIBRARY_MODELS
from .utils import clean_name

log: logging.Logger = logging.getLogger(__name__)
library_blueprint = Blueprint(
    "library", __name__, url_prefix="/lib", template_folder="templates"
)


@library_blueprint.route("/create/<item>")
def create_entry(item: str) -> str:
    model = LIBRARY_MODELS.get(item)
    if not model:
        return "<b>Can't find model type!</b>"
    name = request.args.get("name", type=str)
    if not name:
        log.warning("Missing required argument: name")
        return "Missing required argument: name"
    entry = model(**request.args.to_dict())
    try:
        db.session.add(entry)
        db.session.commit()
        return f"Created: {entry!r}"
    except IntegrityError as exception:
        log.warning(f"Can't add {item}: {exception}")
        return "<b>Creating new entry failed!</b>"


@library_blueprint.route("/read/<item>/<name>")
def read_entry(item: str, name: str) -> str:
    model = LIBRARY_MODELS.get(item)
    if not model:
        return "<b>Can't find model type!</b>"
    entry = model.query.filter_by(name=clean_name(name)).first_or_404()
    return f"Read: {entry!r}"
