import re
from database import db
from flask_login import UserMixin
from flask import flash, url_for
from werkzeug.security import check_password_hash
from sqlalchemy.orm import validates
from helpers import validation_preparation


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

    def __repr__(self):
        return f"User {self.full_name} has email {self.email} and username {self.username}"

    @validates('email')
    @validation_preparation
    def validate_email(self, key, email):
        if not email:
            self.validation_errors.append('No email provided')

        if (not self.email == email):
            if User.query.filter_by(email=email).first():
                self.validation_errors.append('Email is already in use')

        return email

    @validates('username')
    @validation_preparation
    def validate_username(self, key, username):
        if not username:
            self.validation_errors.append('No username provided')
        if (not self.username == username):
            if User.query.filter_by(username=username).first():
                self.validation_errors.append('Username is already in use')

        if len(username) < 5 or len(username) > 20:
            self.validation_errors.append(
                'Username must be between 5 and 20 characters')

        return username

    @validates('password')
    @validation_preparation
    def validate_password(self, key, password):
        if not password:
            self.validation_errors.append('Password not provided')

        if len(password) < 8 or len(password) > 50:
            self.validation_errors.append(
                'Password must be between 8 and 50 characters')

        return password


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
