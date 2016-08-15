from flask_security import login_required
from .base_controller import BaseAuthController


class UserController(BaseAuthController):
    def index(self):
        return self.user.to_dict()

    def logout(self):
        pass
