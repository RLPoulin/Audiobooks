"""Routes for main page module."""

import logging

from flask import Blueprint, Response, abort, make_response, redirect, request
from sqlalchemy.exc import SQLAlchemyError

from audiobooks.extensions import db

from .models import LIBRARY_MODELS, LibraryModel


log: logging.Logger = logging.getLogger(__name__)
library_blueprint = Blueprint(
    "library", __name__, url_prefix="/lib", template_folder="templates"
)


def get_model(item: str) -> type[LibraryModel]:
    """Get the library model corresponding to an item.

    Args:
        item (str): Name of the library model.

    Returns:
        type[LibraryModel]: The library model.

    Raises:
        HTTPError: Raises 404 error if the model is not found.
    """
    return LIBRARY_MODELS.get(item) or abort(404)


def get_record(item: str, record_id: int) -> LibraryModel:
    """Get a record for a library item.

    Args:
        item (str): Name of the library model.
        record_id (int): Record ID of the item.

    Returns:
        LibraryModel: The record.

    Raises:
        HTTPError: Raises 404 error if the record is not found.
    """
    return get_model(item).get_by_id(record_id) or abort(404)


@library_blueprint.route("/<string:item>/find")
def find_by_name(item: str) -> Response:
    """Find a record in the database by name.

    Args:
        item (str): The type of record to find.

    Returns:
        Response: The record.

    Raises:
        HTTPError: Raises 404 error if the record is not found.a
    """
    model: type[LibraryModel] = get_model(item)
    name: str = request.args.get("name", type=str) or abort(404)
    record: LibraryModel = model.get_by_name(name) or abort(404)
    return redirect(f"./{record.record_id}")


@library_blueprint.route("/<string:item>/create")
def create_record(item: str) -> Response:
    """Create new record and add it to the database.

    Args:
        item (str): The type of record to create.

    Returns:
        Response: The record or an error message.

    Raises:
        HTTPError: Raises 400 error if the creation failed.
        HTTPError: Raises 404 error if the model is not found.
    """
    model: type[LibraryModel] = get_model(item)
    try:
        record: LibraryModel = model.create(**request.args.to_dict())
    except (TypeError, ValueError) as exception:
        log.warning(f"Can't create {item}: {exception}")
        abort(400)
    try:
        db.session.commit()
        return redirect(f"./{record.record_id}")
    except SQLAlchemyError as exception:
        db.session.rollback()
        log.warning(f"Can't add {record}: {exception}")
        abort(400)


@library_blueprint.route("/<string:item>/<int:record_id>")
def read_record(item: str, record_id: int) -> Response:
    """Read a record from the database.

    Args:
        item (str): The type of record to read.
        record_id (int): The id of the record.

    Returns:
        Response: The record.

    Raises:
        HTTPError: Raises 404 error if the record is not found.
    """
    record: LibraryModel = get_record(item, record_id)
    return make_response(record.to_dict())


@library_blueprint.route("/<string:item>/<int:record_id>/update")
def update_record(item: str, record_id: int) -> Response:
    """Update a record from the database.

    Args:
        item (str): The type of record to update.
        record_id (int): The id of the record.

    Returns:
        Response: The record or an error message.

    Raises:
        HTTPError: Raises 400 error if the update failed.
        HTTPError: Raises 404 error if the record is not found.
    """
    record: LibraryModel = get_record(item, record_id)
    try:
        record.update(**request.args.to_dict())
    except KeyError as exception:
        log.warning(f"Can't update {item}: {exception}")
        abort(400)
    try:
        db.session.commit()
        return redirect(f"../{record.record_id}")
    except SQLAlchemyError as exception:
        db.session.rollback()
        log.warning(f"Can't update {record}: {exception}")
        abort(400)


@library_blueprint.route("/<string:item>/<int:record_id>/delete")
def delete_record(item: str, record_id: int) -> Response:
    """Delete a record from the database.

    Args:
        item (str): The type of record to delete.
        record_id (int): The id of the record.

    Returns:
        Response: A success or error message.

    Raises:
        HTTPError: Raises 400 error if the deletion failed.
        HTTPError: Raises 404 error if the record is not found.
    """
    record: LibraryModel = get_record(item, record_id)
    try:
        record.delete()
        db.session.commit()
        return make_response("Deleted: {record}")
    except SQLAlchemyError as exception:
        db.session.rollback()
        log.warning(f"Can't delete {record}: {exception}")
        abort(400)
