__all__ = (
    'login_required',
    'admin_permission',
    'member_permission',
)
from flask_login import login_required
from flask_principal import Permission, RoleNeed

admin_permission = Permission(RoleNeed('admin'))
member_permission = Permission(RoleNeed('member'))
