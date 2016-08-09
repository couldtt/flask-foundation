import importlib

from flask import Flask, jsonify
from app.utils import RedisSessionInterface
from app.extensions import (
    api,
    db,
    cache,
    bcrypt,
    celery,
    redis,
    login_manager,
)

from app.handlers import (
    index,
    login,
)
from app.handlers.account_controller import UserController


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.session_interface = RedisSessionInterface()
    register_extensions(app)
    register_error_handlers(app)
    register_middlewares(app)
    register_handlers(app)
    register_controllers()
    api.init_app(app)
    return app


def register_extensions(app):
    db.init_app(app)
    cache.init_app(app)
    bcrypt.init_app(app)
    celery.config_from_object(app.config)
    redis.init_app(app)
    login_manager.init_app(app)


def register_error_handlers(app):
    def render_error(e):
        return jsonify({'code': e.code, 'msg': e.name, 'desc': e.description}), e.code

    for e in (400, 401, 404, 405, 500):
        app.errorhandler(e)(render_error)


def register_middlewares(app):
    mid_mod = importlib.import_module('app.middlewares')
    for middleware in app.config['LOADED_MIDDLEWARES']:
        app.wsgi_app = getattr(mid_mod, middleware)(app.wsgi_app)


def register_url(app, path, endpoint, handler, methods):
    allowed_methods = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTION')
    if not isinstance(methods, list):
        methods = [methods]

    for method in methods:
        if method.upper() not in allowed_methods:
            raise Exception('Invalid method')

    app.add_url_rule(path, endpoint, handler, methods=methods)


def register_handlers(app):
    register_url(app, '/', 'index', index, 'GET')


def register_controllers():
    api.add_resource(UserController, '/user', '/user/<string:method>')
