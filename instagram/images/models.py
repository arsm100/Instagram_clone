from instagram.helpers import s3
from flask import flash, redirect, url_for


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
