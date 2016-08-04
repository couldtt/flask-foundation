from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy
from celery import Celery


cache = Cache()
db = SQLAlchemy()
celery = Celery()
