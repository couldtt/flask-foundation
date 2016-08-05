from flask import Flask
from app.utils import RedisSessionInterface
from app.extensions import (
    db,
    cache,
    bcrypt,
    celery,
)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.session_interface = RedisSessionInterface()
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    cache.init_app(app)
    bcrypt.init_app(app)
    celery.config_from_object(app.config)
