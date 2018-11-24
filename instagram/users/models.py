import re
from instagram import db, S3_LOCATION
from flask_login import UserMixin
from flask import url_for
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from instagram.helpers import validation_preparation


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False, server_default='')
    profile_picture_name = db.Column(
        db.Text, nullable=False, server_default='generic_profile_pic.png')

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

        return password

    @hybrid_property
    def image_url(self):
        return f'{S3_LOCATION}{self.profile_picture_name}'
