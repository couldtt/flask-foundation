__all__ = (
    'api',
    'cache',
    'db',
    'bcrypt',
    'celery',
    'redis',
    'login_manager',
)

from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_redis import FlaskRedis
from flask_login import LoginManager
from celery import Celery
from app.libs.api import CustomApi

api = CustomApi()
cache = Cache()
db = SQLAlchemy()
bcrypt = Bcrypt()
celery = Celery()
redis = FlaskRedis()
login_manager = LoginManager()
