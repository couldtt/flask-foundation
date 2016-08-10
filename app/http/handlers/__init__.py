from flask import redirect, jsonify
from flask_login import login_required, login_user, current_user

from app.models.passport import User
from app.utils import json_resp


@json_resp
@login_required
def index():
    return {'abc': '123'}
    # return 'hello {nickname}'.format(nickname=current_user.nickname)


def login():
    user = User.get_by_id(1)
    login_user(user)
    return redirect('/')


@login_required
def account():
    return jsonify(current_user)
