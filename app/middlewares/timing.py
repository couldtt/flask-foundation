import time


class ResponseTimingMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        start_time = time.time()
        response = self.app(environ, start_response)
        response_time = (time.time() - start_time) * 1000
        data = {
            'path': environ.get('PATH_INFO'),
            'method': environ.get('REQUEST_METHOD'),
            'time': int(response_time)
        }
        print(data)

        return response
