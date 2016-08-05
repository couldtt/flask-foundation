from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from celery import Celery


cache = Cache()
db = SQLAlchemy()
bcrypt = Bcrypt()
celery = Celery()
