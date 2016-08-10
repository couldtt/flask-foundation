from flask_restful import Api
from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_redis import FlaskRedis
from flask_login import LoginManager
from celery import Celery

api = Api()
cache = Cache()
db = SQLAlchemy()
bcrypt = Bcrypt()
celery = Celery()
redis = FlaskRedis()
login_manager = LoginManager()
