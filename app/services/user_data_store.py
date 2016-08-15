__all__ = (
    'user_data_store',
    'RoleContainer',
)
from flask_security import SQLAlchemyUserDatastore as OriginalSQLAlchemyUserDatastore
from app.extensions import db
from app.models.passport import User, Role


class SQLAlchemyUserDatastore(OriginalSQLAlchemyUserDatastore):
    def _prepare_create_user_args(self, **kwargs):
        kwargs.setdefault('is_active', True)
        roles = kwargs.get('roles', [])
        for i, role in enumerate(roles):
            rn = role.name if isinstance(role, self.role_model) else role
            # see if the role exists
            roles[i] = self.find_role(rn)
        kwargs['roles'] = roles
        return kwargs


user_data_store = SQLAlchemyUserDatastore(db, User, Role)


class RoleContainer:
    @classmethod
    def get_super(cls):
        return user_data_store.find_or_create_role('super')

    @classmethod
    def get_seeker(cls):
        return user_data_store.find_or_create_role('seeker')

    @classmethod
    def get_hr(cls):
        return user_data_store.find_or_create_role('hr')

    @classmethod
    def get_admin(cls):
        return user_data_store.find_or_create_role('admin')

    @classmethod
    def get_operation(cls):
        return user_data_store.find_or_create_role('operation')