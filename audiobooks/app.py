"""Base Flask web application."""


from flask import Flask

from audiobooks.extensions import cache, db
from audiobooks.library.routes import library_blueprint
from audiobooks.main_page.routes import main_blueprint


def create_app(config_object: str = "audiobooks.configuration.Config") -> Flask:
    """Create the Flask application and initialize it.

    Args:
        config_object (str, optional): Name of the object containing the app
            configuration. Defaults to "audiobooks.configuration".

    Returns:
        Flask: The Flask application.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app: Flask) -> None:
    """Register all Flask extensions in the application.

    Args:
        app (Flask): The Flask application.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()
    cache.init_app(app)


def register_blueprints(app: Flask) -> None:
    """Register all route blueprints in the application.

    Args:
        app (Flask): The Flask application.
    """
    app.register_blueprint(main_blueprint)
    app.register_blueprint(library_blueprint)
