from instagram.users.models import User
from werkzeug.security import check_password_hash
from flask import flash


def authenticate(username, password):
    try:
        user = User.query.filter_by(username=username).first()
        password_check = check_password_hash(user.password, password)
        if password_check:
            return user
        else:
            flash('Wrong Username/Password!', 'Warning')
    except AttributeError:
        flash('Wrong Username/Password!', 'Warning')
