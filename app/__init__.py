from flask import Flask
from .utils import RedisSessionInterface


def create_app():
    app = Flask(__name__)
    app.session_interface = RedisSessionInterface()
    return app
