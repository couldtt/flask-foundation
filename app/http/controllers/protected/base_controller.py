import copy
import hashlib
from flask import request, abort

from app.config import config
from app.http.controllers.base import (
    BaseController,
    RequestType,
    invalid_return
)

from app.utils.time import get_current_timestamp
from app.utils.encryption import md5
from app.utils.exceptions import HTTPException
from app.utils.logging import get_logger

logger = get_logger('Controller.Protected.Base')


class BaseProtectedController(BaseController):
    def _route(self, request_type, action, **kwargs):
        if action is not None and action.startswith('_'):
            abort(403)

        if action is None:
            action = 'index'

        if request_type == RequestType.GET:
            route_action = action
        else:
            route_action = '_{}_{}'.format(request_type, action)

        m = getattr(self, route_action)
        try:
            data = m(**kwargs)
            return data
        except HTTPException as e:
            return invalid_return(e.name, e.description, e.code)
        except Exception as e:
            logger.error(e)
            abort(500)


class SignatureMixin(object):
    def _get_secret(self, app_id):
        return config['THIRD_APPS'].get(app_id)

    def _check_signature(self):
        app_id = request.headers.get('X-API-APP-ID')
        signature = request.headers.get('X-API-SIGNATURE')
        t = request.headers.get('X-API-TIMESTAMP') or request.args.get('t')

        if t is None or signature is None:
            return False

        try:
            t = int(t)
        except ValueError:
            return False

        current_timestamp = get_current_timestamp()
        if current_timestamp - t > 60:
            return False

        data = request.json.get('data') or request.form.get('data')

        m = hashlib.md5()
        sign = '{0}{1}{2}{3}{4}'.format(request.path.lower(), self._get_secret(app_id), data, request.method.lower(), t)
        m.update(sign.encode('utf-8'))
        sign = m.hexdigest()

        if sign == signature:
            return True
        else:
            return False

    def _check_get_signature(self):
        base_url = request.base_url
        signature = request.headers.get('X-API-SIGNATURE') or request.args.get('signature')
        app_id = request.headers.get('X-API-APP-ID') or request.args.get('app_id')
        t = request.headers.get('X-API-TIMESTAMP') or request.args.get('t')

        if t is None or signature is None:
            return False

        try:
            t = int(t)
        except ValueError:
            return False

        current_timestamp = get_current_timestamp()
        if current_timestamp - t > 60:
            return False

        args = copy.deepcopy(request.args)

        sorted_keys = sorted(args, key=lambda x: x[0])
        string = []
        for key in sorted_keys:
            if key != 'signature':
                string.append('{}={}'.format(key, args[key]))

        sign = md5(base_url + '&'.join(string) + self._get_secret(app_id=app_id))
        if sign == signature:
            return True
        else:
            return False
