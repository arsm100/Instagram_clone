from flask import flash, redirect, url_for
from instagram.helpers import s3
from instagram.users.models import User, UserMixin, db, S3_LOCATION, hybrid_property


class Image(db.Model, UserMixin):

    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, image_name, user_id):
        self.image_name = image_name
        self.user_id = user_id

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
        flash("Something Happened: ", e)
        return redirect(url_for('images.upload'))

    return file.filename
