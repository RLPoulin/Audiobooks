"""Tests for audiobooks.library.routes."""

from flask.testing import FlaskClient

from audiobooks.library.models import Author

from .test_library_models import author  # noqa: F401


URL_PREFIX = "/lib"


def test_find_name__success(client: FlaskClient, author: Author) -> None:
    """Test for route /<item>/find."""
    name = author.name.replace(" ", "%20")
    response = client.get(f"{URL_PREFIX}/author/find?name={name}")
    assert response.status_code == 302
    assert response.headers["Location"] == "./1"


def test_find_name__fail_item(client: FlaskClient, author: Author) -> None:
    """Test for route /<item>/find with invalid item."""
    name = author.name.replace(" ", "%20")
    response = client.get(f"{URL_PREFIX}/FAIL/find?name={name}")
    assert response.status_code == 404


def test_find_name__fail_args(client: FlaskClient, author: Author) -> None:
    """Test for route /<item>/find with invalid arguments."""
    name = author.name.replace(" ", "%20")
    response = client.get(f"{URL_PREFIX}/author/find?FAIL={name}")
    assert response.status_code == 404


def test_find_name__fail_name(client: FlaskClient) -> None:
    """Test for route /<item>/find with invalid name."""
    response = client.get(f"{URL_PREFIX}/author/find?name=FAIL")
    assert response.status_code == 404


def test_create__success(client: FlaskClient) -> None:
    """Test for route /<item>/create."""
    response = client.get(f"{URL_PREFIX}/author/create?name=Test")
    assert response.status_code == 302
    assert response.headers["Location"] == "./1"


def test_create__fail_args(client: FlaskClient) -> None:
    """Test for route /<item>/create with invalid arguments."""
    response = client.get(f"{URL_PREFIX}/author/create?FAIL=FAIL")
    assert response.status_code == 400


def test_create__fail_duplicate(client: FlaskClient, author: Author) -> None:
    """Test for route /<item>/create with duplicate name."""
    name = author.name.replace(" ", "%20")
    response = client.get(f"{URL_PREFIX}/author/create?name={name}")
    assert response.status_code == 400


def test_read__success(client: FlaskClient, author: Author) -> None:
    """Test for route /<item>/<record_id>."""
    response = client.get(f"{URL_PREFIX}/author/{author.record_id}")
    assert response.status_code == 200


def test_read__failure(client: FlaskClient, author: Author) -> None:
    """Test for route /<item>/<record_id> with invalid id."""
    response = client.get(f"{URL_PREFIX}/author/999")
    assert response.status_code == 404


def test_update__success(client: FlaskClient, author: Author) -> None:
    """Test for route /<item>/<record_id>/update."""
    response = client.get(f"{URL_PREFIX}/author/{author.record_id}/update?name=Test")
    assert response.status_code == 302
    assert response.headers["Location"] == f"../{author.record_id}"


def test_update__fail_args(client: FlaskClient, author: Author) -> None:
    """Test for route /<item>/<record_id>/update with invalid arguments."""
    response = client.get(f"{URL_PREFIX}/author/{author.record_id}/update?FAIL=FAIL")
    assert response.status_code == 400


def test_update__fail_duplicate(client: FlaskClient, author: Author) -> None:
    """Test for route /<item>/<record_id>/update with duplicate name."""
    client.get(f"{URL_PREFIX}/author/create?name=TEST")
    response = client.get(f"{URL_PREFIX}/author/{author.record_id}/update?name=TEST")
    assert response.status_code == 400


def test_delete__success(client: FlaskClient, author: Author) -> None:
    """Test for route /<item>/<record_id>/delete."""
    response = client.get(f"{URL_PREFIX}/author/{author.record_id}/delete")
    assert response.status_code == 200
