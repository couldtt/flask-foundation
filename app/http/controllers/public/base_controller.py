from flask import abort
from flask_login import current_user
from werkzeug.exceptions import (
    HTTPException,
    BadRequest,
)

from app.http.controllers.base import (
    BaseController,
    RequestType,
    invalid_return,
)
from app.http.permissions import (
    admin_permission,
    member_permission,
    login_required,
)

from app.utils.exceptions import custom_exceptions
from app.utils import get_logger

logger = get_logger('Controller.Public.Base')


class BasePublicController(BaseController):
    def __init__(self):
        super(BasePublicController, self).__init__()
        self.user = current_user

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


class BaseBackendAuthController(BasePublicController):
    method_decorators = [admin_permission.require(http_exception=403), login_required]


class BaseFrontendAuthController(BasePublicController):
    method_decorators = [member_permission.require(http_exception=403), login_required]
