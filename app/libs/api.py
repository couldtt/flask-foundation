from flask_restful import Api


class CustomApi(Api):
    def handle_error(self, e):
        raise e
