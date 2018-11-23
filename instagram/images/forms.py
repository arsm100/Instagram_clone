from flask_wtf import FlaskForm, Form
from flask_wtf.csrf import CsrfProtect
from wtforms import StringField, FileField, SubmitField


class UploadForm(FlaskForm):
    user_photo = FileField('User Photo')
    submit = SubmitField('Submit')
