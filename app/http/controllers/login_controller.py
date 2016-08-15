from flask_login import login_user

from app.http.controllers.base_controller import BaseController


class LoginController(BaseController):
    def _post_index(self, username: list, password: str):
        pass

    def _post_wechat(self):
        pass

    def _post_mobile(self):
        pass
