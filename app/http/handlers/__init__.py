from flask import redirect, jsonify
from flask_login import login_required, login_user, current_user
from app import login_manager
from app.models.passport import User


@login_manager.user_loader
def user_loader(user_id):
    return User.get_by_id(user_id)


@login_required
def index():
    return 'hello {nickname}'.format(nickname=current_user.nickname)


def login():
    user = User.get_by_id(1)
    login_user(user)
    return redirect('/')


@login_required
def account():
    return jsonify(current_user)

