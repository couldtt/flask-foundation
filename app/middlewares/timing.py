from time import monotonic
from app.utils import get_logger

logger = get_logger('Middleware.Timing')


class ResponseTimingMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        start_time = monotonic()
        response = self.app(environ, start_response)
        response_time = (monotonic() - start_time) * 1000
        data = {
            'path': environ.get('PATH_INFO'),
            'method': environ.get('REQUEST_METHOD'),
            'time': int(response_time)
        }
        logger.info(data)

        return response
