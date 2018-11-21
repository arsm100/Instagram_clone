from flask_wtf import FlaskForm, Form
from flask_wtf.csrf import CsrfProtect
from wtforms import StringField, PasswordField, SubmitField, validators


class SignupForm(FlaskForm):
    full_name = StringField('Full Name', [validators.InputRequired()])
    email = StringField('Email', [validators.InputRequired()])
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField('Submit')


class EditForm(FlaskForm):
    full_name = StringField('Full Name', [validators.InputRequired()])
    email = StringField('Email', [validators.InputRequired()])
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField('Submit')


class DeleteForm(FlaskForm):
    submit = SubmitField('Submit')
