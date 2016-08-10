class RequestFrequencyMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        response = self.app(environ, start_response)
        return response
