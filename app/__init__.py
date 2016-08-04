from flask import Flask
from app.utils import RedisSessionInterface
from app.extensions import (
    db,
    cache,
    celery,
)


def create_app():
    app = Flask(__name__)
    app.session_interface = RedisSessionInterface()
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    cache.init_app(app)
    celery.config_from_object(app.config)
