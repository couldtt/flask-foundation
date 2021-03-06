from flask_principal import identity_changed, Identity
from flask_login import login_user
from flask import abort, current_app

from app.http.controllers.public.base_controller import BasePublicController
from app.libs.response import Response
from app.services import user_data_store


class LoginController(BasePublicController):
    def _post_index(self, username: str, password: str):
        user = user_data_store.find_user(username=username)
        if user is None:
            abort(401)

        if not user.check_password(password):
            abort(401)

        try:
            login_user(user)
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))

            return Response.success()
        except:
            abort(500)

    def _post_wechat(self):
        pass

    def _post_mobile(self):
        pass
