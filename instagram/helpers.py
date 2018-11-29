import boto3
import botocore
from instagram import S3_KEY, S3_SECRET, S3_BUCKET, current_user, sg
from sendgrid.helpers.mail import *

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


s3 = boto3.client('s3', aws_access_key_id=S3_KEY,
                  aws_secret_access_key=S3_SECRET)


def delete_photo(image_name):
    s3.delete_object(
        Bucket=S3_BUCKET,
        Key=image_name)


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


def send_donation_email(to, amount):
    from_email = Email("donations@aragram.com")
    to_email = Email(to)
    subject = f"Thank You For Your Donation {current_user.username}"
    content = Content(
        "text/html", f"Dear {current_user.full_name},\n \n You have just donated{amount} USD on Aragram. \n Thank you for your generosity and we wish you a continued pleasant experience with Aragram. \n \n Kind regards,\n Aragram Team")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    # print(response.status_code)
    # print(response.body)
    # print(response.headers)


def send_signup_email(to):
    from_email = Email("signup@aragram.com")
    to_email = Email(to)
    subject = f"Welcome to Aragram {current_user.username}"
    content = Content(
        "text/html", f"Dear {current_user.full_name},\n \n You have just signed up on Aragram! \n We encourage you to start uploading your pictures and hopefully make some money as well as get to see the work of other up-and-coming creators just like yourself. \n We wish you the most pleasant of experiences with Aragram. \n \n Kind regards,\n Aragram Team")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    # print(response.status_code)
    # print(response.body)
    # print(response.headers)
