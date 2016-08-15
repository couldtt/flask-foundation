from flask import abort
from flask_login import logout_user
from .base_controller import BaseAuthController
from app.libs.response import Response
from app.utils import get_logger

logger = get_logger('Controller.User')


class UserController(BaseAuthController):
    def index(self):
        return self.user.to_dict()

    def _post_logout(self):
        try:
            logout_user()
            return Response.success()
        except Exception as ex:
            logger.error(ex)
            abort(500)
