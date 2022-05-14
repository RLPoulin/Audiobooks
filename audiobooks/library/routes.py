"""Routes for main page module."""

import logging

from flask import Blueprint, Response, abort, make_response, redirect, request

from audiobooks.extensions import db

from .models import LIBRARY_MODELS, LibraryModel

log: logging.Logger = logging.getLogger(__name__)
library_blueprint = Blueprint(
    "library", __name__, url_prefix="/lib", template_folder="templates"
)


@library_blueprint.route("/<string:item>/create")
def create_entry(item: str) -> Response:
    model: type[LibraryModel] = LIBRARY_MODELS.get(item) or abort(404)
    record: LibraryModel = model.create(**request.args.to_dict())
    try:
        db.session.commit()
        return redirect(f"./{record.record_id}")
    except Exception as exception:  # noqa: B902
        db.session.rollback()
        log.warning(f"Can't add {record}: {exception}")
        return make_response(f"<b>Creating {record} failed!</b><p>{exception}")


@library_blueprint.route("/<string:item>/find")
def find_by_name(item: str) -> Response:
    model: type[LibraryModel] = LIBRARY_MODELS.get(item) or abort(404)
    name: str = request.args.get("name", type=str) or abort(404)
    record: LibraryModel = model.get_by_name(name) or abort(404)
    return redirect(f"./{record.record_id}")


@library_blueprint.route("/<string:item>/<int:record_id>")
def read_record(item: str, record_id: int) -> Response:
    model: type[LibraryModel] = LIBRARY_MODELS.get(item) or abort(404)
    record: LibraryModel = model.get_by_id(record_id) or abort(404)
    return make_response(record.to_dict())


@library_blueprint.route("/<string:item>/<int:record_id>/update")
def update_record(item: str, record_id: int) -> Response:
    model: type[LibraryModel] = LIBRARY_MODELS.get(item) or abort(404)
    record: LibraryModel = model.get_by_id(record_id) or abort(404)
    try:
        record.update(**request.args.to_dict())
        db.session.commit()
        return redirect(f"../{record.record_id}")
    except Exception as exception:  # noqa: B902
        db.session.rollback()
        log.warning(f"Can't update {record}: {exception}")
        return make_response(f"<b>Updating {record} failed!</b><p>{exception}")


@library_blueprint.route("/<string:item>/<int:record_id>/delete")
def delete_record(item: str, record_id: int) -> Response:
    model: type[LibraryModel] = LIBRARY_MODELS.get(item) or abort(404)
    record: LibraryModel = model.get_by_id(record_id) or abort(404)
    try:
        record.delete()
        db.session.commit()
        return f"Deleted: {record}"
    except Exception as exception:  # noqa: B902
        db.session.rollback()
        log.warning(f"Can't delete {record}: {exception}")
        return make_response(f"<b>Deleting {record} failed!</b><p>{exception}")
