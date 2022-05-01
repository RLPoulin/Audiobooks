"""Extensions module. Each extension is initialized in app.create_app()"""
import flask_caching
import flask_migrate
import flask_sqlalchemy

cache = flask_caching.Cache()
db = flask_sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate()
