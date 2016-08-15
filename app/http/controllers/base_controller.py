from flask import abort
from flask_restful import Resource, reqparse
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
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
                return invalid_return('invalid param', '参数格式错误', 400)
            except Exception as e:
                logger.error(e)
                return invalid_return('parse error', '参数解析错误', 400)

            try:
                data = m(**args)
                return data
            except TypeError as e:
                e = str(e)
                logger.info(e)
                param = e.split(' ')[-1].strip("'") if e.startswith(route_action) else None
                if param is not None:
                    return invalid_return('missing param [{}]'.format(param), '{}参数缺失'.format(param), 400)
                else:
                    abort(500)
            except HTTPException as e:
                return invalid_return(e.name, e.description, e.code)
            except Exception as e:
                logger.error(e)
                abort(500)
        else:
            abort(404)


admin_permission = Permission(RoleNeed('admin'))
member_permission = Permission(RoleNeed('member'))


class BaseBackendAuthController(BaseController):
    method_decorators = [login_required, admin_permission.require(http_exception=403)]


class BaseFrontendAuthController(BaseController):
    method_decorators = [login_required, member_permission.require(http_exception=403)]
