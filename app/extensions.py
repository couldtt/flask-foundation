from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from celery import Celery
from redis import StrictRedis


cache = Cache()
db = SQLAlchemy()
bcrypt = Bcrypt()
celery = Celery()
redis = StrictRedis()
