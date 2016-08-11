from flask import abort
from flask_restful import Resource, reqparse
from flask_login import current_user, login_required
from werkzeug.exceptions import HTTPException

from app.utils.exceptions import custom_exceptions


class RequestType:
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'
    OPTION = 'option'
    HEAD = 'head'


class BaseResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()


class BaseController(BaseResource):
    def __init__(self):
        super(BaseController, self).__init__()
        self.user = current_user

    def get(self, action=None, **kwargs):
        return self._route(RequestType.GET, action, **kwargs)

    def post(self, action=None, **kwargs):
        return self._route(RequestType.POST, action, **kwargs)

    def put(self, action=None, **kwargs):
        return self._route(RequestType.PUT, action, **kwargs)

    def patch(self, action=None, **kwargs):
        return self._route(RequestType.PATCH, action, **kwargs)

    def delete(self, action=None, **kwargs):
        return self._route(RequestType.DELETE, action, **kwargs)

    def _route(self, request_type, action, **kwargs):
        if action is not None and action.startswith('_'):
            abort(403)

        if action is None:
            action = 'index'

        if request_type == RequestType.GET:
            route_action = action
        else:
            route_action = '_{}_{}'.format(request_type, action)

        if hasattr(self, route_action):
            m = getattr(self, route_action)
            try:
                data = m(**kwargs)
                return data
            except HTTPException as e:
                return {
                           'msg': e.name,
                           'description': custom_exceptions.get(
                               e.code).description if e.code in custom_exceptions else e.description,
                       }, e.code
        else:
            abort(404)


class BaseAuthController(BaseController):
    method_decorators = [login_required]
