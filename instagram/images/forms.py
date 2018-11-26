from flask_wtf import FlaskForm, Form
from flask_wtf.csrf import CsrfProtect
from wtforms import FileField, StringField, SubmitField


class UploadForm(FlaskForm):
    user_photo = FileField('User Photo')
    image_caption = StringField('Image Caption')
    submit = SubmitField('Submit')
