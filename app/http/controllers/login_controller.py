from app.http.controllers.base_controller import BaseController


class LoginController(BaseController):
    def _post_index(self):
        self.parser.add_argument('username')
        self.parser.add_argument('password')
        args = self.parser.parse_args()
        return args

    def _post_wechat(self):
        pass

    def _post_mobile(self):
        pass
