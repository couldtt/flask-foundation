from flask_security import login_required
from .base_controller import BaseAuthController


class UserController(BaseAuthController):
    def index(self):
        return {'nickname': getattr(self.user, 'nickname', '匿名')}

    def logout(self):
        pass
