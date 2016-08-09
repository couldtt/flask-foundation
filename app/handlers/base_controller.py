from flask_login import current_user

class BaseController:

    def __init__(self):
        self.user = current_user
