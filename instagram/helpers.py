import boto3
import botocore
from instagram import S3_KEY, S3_SECRET, S3_BUCKET

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
s3 = boto3.client('s3', aws_access_key_id=S3_KEY,
                  aws_secret_access_key=S3_SECRET)


def validation_preparation(func):
    def wrapper(obj, key, value):
        try:
            obj.validation_errors
        except AttributeError:
            obj.validation_errors = []
        return func(obj, key, value)

    return wrapper


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
