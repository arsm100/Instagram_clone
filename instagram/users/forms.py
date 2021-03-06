from flask_wtf import FlaskForm
from flask_wtf.csrf import CsrfProtect
from wtforms import StringField, PasswordField, SubmitField


class SignupForm(FlaskForm):
    full_name = StringField('Full Name')
    email = StringField('Email')
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')


class EditForm(FlaskForm):
    full_name = StringField('Full Name')
    email = StringField('Email')
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')


class DeleteForm(FlaskForm):
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    query = StringField('Search')
    submit = SubmitField('Submit')

    class Meta:
        cstf = False
