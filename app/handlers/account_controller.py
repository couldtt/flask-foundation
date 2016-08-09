from .base_controller import BaseController


class UserController(BaseController):
    def index(self):
        return self.user.nickname

    def _post_reset_password(self):
        return 'post reset password'

    def _post_profile(self):
        return 'post method'
