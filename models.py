from database import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    def __init__(self, full_name, email, username, password):
        self.full_name = full_name
        self.email = email
        self.username = username
        self.password = password

    def get_id(self):
        return self.username

    def __repr__(self):
        return f"User {self.full_name} has email {self.email} and username {self.username}"


def authenticate(username, password):
    try:
        user = User.query.filter_by(username=username).all()[0]
        password_check = check_password_hash(user.password, password)
        if password_check:
            return user
        else:
            flash('Wrong Username/Password!', 'Warning')
    except IndexError:
        flash('Wrong Username/Password!', 'Warning')
