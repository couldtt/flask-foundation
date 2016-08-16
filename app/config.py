import os

SITE_NAME = 'Flask-Foundation'
ENV_SYMBOL_NAME = 'FF'


class base_config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', '!@#12356789!@$XAQWQ@dfi')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_ECHO = True

    REDIS_HOST = os.environ.get('REDIS_TCP_ADDR', '127.0.0.1')
    REDIS_PORT = os.environ.get('REDIS_TCP_PORT', 6379)

    REDIS_URL = 'redis://{}:{}'.format(REDIS_HOST, REDIS_PORT)
    BROKER_URL = REDIS_URL
    BROKER_BACKEND = BROKER_URL

    CACHE_HOST = os.environ.get('CACHE_ENV_HOST', '127.0.0.1')
    CACHE_PORT = os.environ.get('CACHE_ENV_PORT', 6379)
    CACHE_TYPE = 'redis'

    POSTGRES_HOST = os.environ.get('DB_ENV_HOST', '127.0.0.1')
    POSTGRES_PORT = os.environ.get('DB_ENV_PORT', '5432')
    POSTGRES_USER = os.environ.get('DB_ENV_USER', 'postgres')
    POSTGRES_PASS = os.environ.get('DB_ENV_PASS', 'postgres')
    POSTGRES_DB = os.environ.get("DB_ENV_NAME", 'ff')

    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % (
        POSTGRES_USER,
        POSTGRES_PASS,
        POSTGRES_HOST,
        POSTGRES_PORT,
        POSTGRES_DB
    )

    LOADED_MIDDLEWARE = (
        'RequestFrequencyMiddleware',
        'ResponseTimingMiddleware',
    )

    THIRD_APPS = {
        'app_id': '_______________app_secret______________',
    }


class dev_config(base_config):
    """Development configuration options."""
    DEBUG = True
    ASSETS_DEBUG = True
    WTF_CSRF_ENABLED = False


class test_config(base_config):
    """Testing configuration options."""
    TESTING = True
    WTF_CSRF_ENABLED = False


configs = {
    'dev': dev_config,
    'test': test_config
}

config = configs.get(os.environ.get(ENV_SYMBOL_NAME, 'dev'))
config.SITE_NAME = SITE_NAME
