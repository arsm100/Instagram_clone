from flask_wtf import FlaskForm
from flask_wtf.csrf import CsrfProtect
from wtforms import FileField, StringField, PasswordField, SubmitField


class UploadForm(FlaskForm):
    user_photo = FileField('User Photo')
    image_caption = StringField('Image Caption')
    submit = SubmitField('Submit')


class EditCaptionForm(FlaskForm):
    image_caption = StringField('Image Caption')
    submit = SubmitField('Submit')


class DeleteForm(FlaskForm):
    submit = SubmitField('Submit')
