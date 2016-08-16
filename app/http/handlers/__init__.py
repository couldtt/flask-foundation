from app.http.permissions import (
    member_permission,
    admin_permission,
    login_required
)

from app.utils import json_resp


@json_resp
@member_permission.require(http_exception=403)
@login_required
def index():
    return 'Hello, Flask'
