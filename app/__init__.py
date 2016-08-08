from flask import Flask, jsonify
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
    register_error_handlers(app)
    return app


def register_extensions(app):
    db.init_app(app)
    cache.init_app(app)
    bcrypt.init_app(app)
    celery.config_from_object(app.config)


def register_error_handlers(app):
    def render_error(e):
        return jsonify({'code': e.code, 'msg': e.name, 'desc': e.description}), e.code

    for e in (400, 401, 404, 500):
        app.errorhandler(e)(render_error)
