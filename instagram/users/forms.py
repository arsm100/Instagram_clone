from flask_wtf import FlaskForm, Form
from flask_wtf.csrf import CsrfProtect
from wtforms import StringField, PasswordField, SubmitField, validators


class SignupForm(FlaskForm):
    full_name = StringField('Full Name')
    email = StringField('Email')
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')