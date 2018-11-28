from flask import flash, redirect, url_for
from instagram.helpers import s3
from instagram.users.models import User, UserMixin, db, S3_LOCATION, hybrid_property
from flask_login import current_user


class Image(db.Model, UserMixin):

    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_caption = db.Column(db.Text, nullable=True)
    donations = db.relationship("Donation", backref="images", lazy='dynamic')

    def __init__(self, image_name, user_id, image_caption=None):
        self.user_id = user_id
        self.image_name = f'{self.user_id}.{self.id}.{image_name}'
        self.image_caption = image_caption

    @hybrid_property
    def images_url(self):
        return f'{S3_LOCATION}{self.image_name}'


def upload_file_to_s3(file, bucket_name, acl="public-read"):

    # Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is to catch all exception
        return redirect(url_for('users.profile', id=current_user.id))

    return file.filename
