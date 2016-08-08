import logging
import logging.config


def get_logger(server_name):
    config = {
        'version': 1,
        'formatters': {
            'verbose': {
                "format": "[%(process)s-%(thread)d][%(levelname)s][%(module)s-%(lineno)d]%(asctime)s %(name)s:%(message)s"
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose"
            },
        },
        "loggers": {
            "Service": {
                "handlers": ["console"],
                "propagate": False,
                "level": "DEBUG"
            },
        }
    }
    logging.config.dictConfig(config)
    return logging.getLogger('Service.' + server_name)
