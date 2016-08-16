__all__ = (
    'invalid_return',
    'RequestType',
    'BaseResource',
)

from functools import partial
from collections import OrderedDict
from flask import request, Response as ResponseBase
from flask_restful import Resource, reqparse
from flask_restful.utils import unpack


def invalid_return(msg, description, status_code):
    return {
               'msg': msg,
               'description': description
           }, status_code


class RequestType:
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'
    OPTION = 'option'
    HEAD = 'head'


class BaseController(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def dispatch_request(self, *args, **kwargs):

        # Taken from flask
        # noinspection PyUnresolvedReferences

        action = kwargs.get('action')
        if action:
            del kwargs['action']
        meth = partial(self._route, request.method.lower(), action)

        for decorator in self.method_decorators:
            meth = decorator(meth)

        resp = meth(*args, **kwargs)

        if isinstance(resp, ResponseBase):  # There may be a better way to test
            return resp

        representations = self.representations or OrderedDict()

        # noinspection PyUnresolvedReferences
        mediatype = request.accept_mimetypes.best_match(representations, default=None)
        if mediatype in representations:
            data, code, headers = unpack(resp)
            resp = representations[mediatype](data, code, headers)
            resp.headers['Content-Type'] = mediatype
            return resp

        return resp

    def _route(self, request_type, action, *kwargs):
        pass

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

    def option(self):
        pass
