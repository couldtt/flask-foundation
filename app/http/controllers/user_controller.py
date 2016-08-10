from flask_security import login_required
from .base_controller import BaseController
from app.utils.exceptions import BadRequest


class UserController(BaseController):
    @login_required
    def index(self):
        return {'nickname': getattr(self.user, 'nickname', '匿名')}

    def avatars(self):
        return {
            'img1': 'http://www.baixing.com/logo.png'
        }

    def _post_reset_password(self):
        return 'post reset password'

    def _post_profile(self):
        return 'post method'
