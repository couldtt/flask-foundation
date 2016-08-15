from flask import abort
from flask_restful import Resource, reqparse
from flask_login import current_user, login_required
from werkzeug.exceptions import HTTPException, BadRequest

from app.utils.exceptions import custom_exceptions
from app.utils import get_logger

logger = get_logger('Controller.Base')


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
            location = 'args'
        else:
            route_action = '_{}_{}'.format(request_type, action)
            location = 'json'

        if hasattr(self, route_action):
            m = getattr(self, route_action)
            annotations = m.__annotations__
            logger.info(annotations)
            for key_, type_ in annotations.items():
                if key_ != 'return':
                    self.parser.add_argument(key_, type=type_, location=location)
            try:
                original_args = self.parser.parse_args()
                args = {key: val for key, val in original_args.items() if val is not None}
            except BadRequest:
                return invalid_return('invalid param', '参数错误', 400)

            try:
                data = m(**args)
                return data
            except TypeError as e:
                logger.info(e)
                param = str(e).split(' ')[-1].strip("'")
                return invalid_return('missing param [{}]'.format(param), '{}参数缺失'.format(param), 400)
            except HTTPException as e:
                return invalid_return(e.name, custom_exceptions.get(
                    e.code).description if e.code in custom_exceptions else e.description, e.code)
            except Exception as e:
                logger.error(e)
                abort(500)
        else:
            abort(404)


class BaseAuthController(BaseController):
    method_decorators = [login_required]
