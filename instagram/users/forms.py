from flask_wtf import FlaskForm, Form
from flask_wtf.csrf import CsrfProtect
from wtforms import StringField, PasswordField, SubmitField, validators


class SignupForm(FlaskForm):
    full_name = StringField('Full Name', [validators.InputRequired('Full name is a required field')])
    email = StringField('Email')
    username = StringField('Username')
    password = PasswordField('Password', [
                             validators.Length(8, 50, 'Password must be between 8 and 50 characters')])
    submit = SubmitField('Submit')


class EditForm(FlaskForm):
    full_name = StringField('Full Name', [validators.InputRequired('Full name is a required field')])
    email = StringField('Email')
    username = StringField('Username')
    password = PasswordField('Password', [
                             validators.Length(8, 50, 'Password must be between 8 and 50 characters')])
    submit = SubmitField('Submit')


class DeleteForm(FlaskForm):
    submit = SubmitField('Submit')
