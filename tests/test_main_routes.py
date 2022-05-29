"""Tests for audiobooks.main_page.routes."""

from flask.testing import FlaskClient


URL_PREFIX = ""


def test_hello(client: FlaskClient) -> None:
    """Test for route /."""
    response = client.get(f"{URL_PREFIX}/")
    assert response.status_code == 200
