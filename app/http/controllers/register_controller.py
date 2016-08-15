from werkzeug.exceptions import abort

from app.http.controllers.base_controller import BaseController
from app.services import user_data_store, RoleContainer
from app.extensions import bcrypt, db
from app.utils.exceptions import Conflict

from app.utils import get_logger

logger = get_logger('Controller.Register')


class RegisterController(BaseController):
    def _post_index(self, username: str, password: str):
        user = user_data_store.find_user(username=username)
        if user is not None:
            raise Conflict(description='用户名冲突')
        else:
            try:
                user = user_data_store.create_user(
                    username=username,
                    pw_hash=bcrypt.generate_password_hash(password).decode('utf-8'),
                    roles=[RoleContainer.get_seeker()]
                )
                user_data_store.commit()
                return {
                    'id': user.id,
                    'user': user.username
                }
            except Exception as ex:
                db.session.rollback()
                logger.error(ex)
                abort(500)
