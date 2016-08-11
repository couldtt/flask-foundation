from flask import redirect, jsonify, request
from flask_login import login_required, login_user, current_user

from app.models.passport import User
from app.utils import json_resp


@json_resp
@login_required
def index():
    return 'hello'


