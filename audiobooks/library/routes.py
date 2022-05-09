"""Routes for main page module."""

import logging

from flask import Blueprint, abort, redirect, request

from audiobooks.extensions import db

from .models import LIBRARY_MODELS

log: logging.Logger = logging.getLogger(__name__)
library_blueprint = Blueprint(
    "library", __name__, url_prefix="/lib", template_folder="templates"
)


@library_blueprint.route("/<string:item>/create")
def create_entry(item: str) -> str:
    model = LIBRARY_MODELS.get(item) or abort(404)
    record = model.create(**request.args.to_dict())
    try:
        db.session.commit()
        return redirect(f"./{record.record_id}")
    except Exception as exception:  # noqa: B902
        db.session.rollback()
        log.warning(f"Can't add {record}: {exception}")
        return "<b>Creating new record failed!</b>"


@library_blueprint.route("/<string:item>/find")
def find_by_name(item: str) -> str:
    model = LIBRARY_MODELS.get(item) or abort(404)
    name = request.args.get("name", type=str) or abort(404)
    record = model.get_by_name(name) or abort(404)
    return redirect(f"./{record.record_id}")


@library_blueprint.route("/<string:item>/<int:record_id>")
def read_record(item: str, record_id: int) -> str:
    model = LIBRARY_MODELS.get(item) or abort(404)
    record = model.get_by_id(record_id) or abort(404)
    return record.to_dict()


@library_blueprint.route("/<string:item>/<int:record_id>/update")
def update_record(item: str, record_id: int) -> str:
    model = LIBRARY_MODELS.get(item) or abort(404)
    record = model.get_by_id(record_id) or abort(404)
    try:
        record.update(**request.args.to_dict())
        db.session.commit()
        return redirect(f"../{record.record_id}")
    except Exception as exception:  # noqa: B902
        db.session.rollback()
        log.warning(f"Can't update {record}: {exception}")
        return "<b>Updating record failed!</b>"


@library_blueprint.route("/<string:item>/<int:record_id>/delete")
def delete_record(item: str, record_id: int) -> str:
    model = LIBRARY_MODELS.get(item) or abort(404)
    record = model.get_by_id(record_id) or abort(404)
    try:
        record.delete()
        db.session.commit()
        return f"Deleted: {record}"
    except Exception as exception:  # noqa: B902
        db.session.rollback()
        log.warning(f"Can't delete {record}: {exception}")
        return "<b>Deleting record failed!</b>"
