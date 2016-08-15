from flask import abort, current_app
from flask.ext.principal import AnonymousIdentity, identity_changed
from flask_login import logout_user
from .base_controller import BaseFrontendAuthController
from app.libs.response import Response
from app.utils import get_logger

logger = get_logger('Controller.User')


class UserController(BaseFrontendAuthController):
    def index(self):
        return self.user.to_dict()

    def _post_logout(self):
        try:
            logout_user()
            identity_changed.send(current_app._get_current_object(),
                                  identity=AnonymousIdentity())
            return Response.success()
        except Exception as ex:
            logger.error(ex)
            abort(500)
