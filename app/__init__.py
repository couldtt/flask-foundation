import importlib
from functools import partial

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
from app.urls import (
    handlers,
    controllers,
    resources
)


def create_app(config, is_web=True):
    app = Flask(__name__)
    app.config.from_object(config)
    app.session_interface = RedisSessionInterface()
    register_extensions(app)
    if is_web:
        register_web(app)

    return app


def register_web(app):
    register_error_handlers(app)
    register_middleware(app)
    register_handlers(app)
    register_controllers()
    register_resource()
    api.init_app(app)


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


def register_middleware(app):
    mid_mod = importlib.import_module('app.middleware')
    for middleware in app.config['LOADED_MIDDLEWARE']:
        app.wsgi_app = getattr(mid_mod, middleware)(app.wsgi_app)


def register_handlers(app):
    def add_url_rule(app, path, endpoint, handler, methods):
        allowed_methods = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTION')
        if not isinstance(methods, list):
            methods = [methods]

        for method in methods:
            if method.upper() not in allowed_methods:
                raise Exception('Invalid method')

        app.add_url_rule(path, endpoint, handler, methods=methods)

    register_handler = partial(add_url_rule, app)
    for handler in handlers:
        register_handler(*handler)


def register_controllers():
    def register_controller(controller, url):
        api.add_resource(controller, url, '{}/<string:method>'.format(url))

    for controller in controllers:
        register_controller(*controller)


def register_resource():
    pass
