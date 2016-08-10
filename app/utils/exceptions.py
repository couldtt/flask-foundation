from werkzeug.exceptions import HTTPException

__all__ = []
custom_exceptions = {}


class BadRequest(HTTPException):
    code = 400
    description = '参数有误'


class Unauthorized(HTTPException):
    code = 401
    description = '请登录后再进行操作'


class NotFound(HTTPException):
    code = 404
    description = '找不到该条数据'


class Forbidden(HTTPException):
    code = 403
    description = '没有操作权限'


class MethodNotAllowed(HTTPException):
    code = 405
    description = '不允许的操作方法'

    def __init__(self, valid_methods=None, description=None):
        """Takes an optional list of valid http methods
        starting with werkzeug 0.3 the list will be mandatory."""
        HTTPException.__init__(self, description)
        self.valid_methods = valid_methods

    def get_headers(self, environ):
        headers = HTTPException.get_headers(self, environ)
        if self.valid_methods:
            headers.append(('Allow', ', '.join(self.valid_methods)))
        return headers


class NotAcceptable(HTTPException):
    code = 406

    description = '请求无法接受'


class RequestTimeout(HTTPException):
    code = 408
    description = '请求超时'


class Conflict(HTTPException):
    code = 409
    description = '请求冲突, 不允许的状态变更'


class Gone(HTTPException):
    code = 410
    description = (
        'The requested URL is no longer available on this server and there '
        'is no forwarding address. If you followed a link from a foreign '
        'page, please contact the author of this page.'
    )


class LengthRequired(HTTPException):
    code = 411
    description = '请检查Content-Length'


class TooManyRequests(HTTPException):
    code = 429
    description = '请求频率到达上限, 请稍后再进行访问'


class InternalServerError(HTTPException):
    code = 500
    description = '服务器内部错误'


class NotImplemented(HTTPException):
    code = 501
    description = '该方法尚未实现'


class BadGateway(HTTPException):
    code = 502
    description = '网关错误'


class ServiceUnavailable(HTTPException):
    code = 503
    description = '服务临时不可访问, 请稍后重试'


class GatewayTimeout(HTTPException):
    code = 504
    description = '网关超时'


def _find_exceptions():
    for name, obj in iter(globals().items()):
        try:
            is_http_exception = issubclass(obj, HTTPException)
        except TypeError:
            is_http_exception = False
        if not is_http_exception or obj.code is None:
            continue
        __all__.append(obj.__name__)
        old_obj = custom_exceptions.get(obj.code, None)
        if old_obj is not None and issubclass(obj, old_obj):
            continue
        custom_exceptions[obj.code] = obj


_find_exceptions()
del _find_exceptions
