from instagram.helpers import allowed_file, S3_BUCKET
from instagram.images.models import upload_file_to_s3
from flask import Blueprint, render_template, request, redirect, url_for, flash, escape, sessions
from instagram.images.forms import UploadForm
from flask_login import current_user
from werkzeug.utils import secure_filename
from instagram.users.models import User
from instagram import db


images_blueprint = Blueprint(
    'images', __name__, template_folder='templates/')


@images_blueprint.route("<id>/profile_picture", methods=['GET'])
def upload(id):
    form = UploadForm()
    return render_template('images/upload.html', form=form)


@images_blueprint.route("<id>/new", methods=['POST'])
def upload_image(id):
    if current_user.username in ('ahmedramzy160', 'josh777') or int(id) == current_user.id:

            # check there is a file
        if "user_photo" not in request.files:
            flash("No photo was uploaded")
            return redirect(url_for('upload'))

            # grab the photo
        file = request.files["user_photo"]

        # check there is a name
        if file.filename == "":
            flash("Please upload your photo!")
            return redirect(url_for('upload'))

            # check correct extension and upload if valid
        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)
            output = upload_file_to_s3(file, S3_BUCKET)
            editted_user = User.query.get(current_user.id)
            editted_user.profile_picture_URL = str(output)
            db.session.add(editted_user)
            db.session.commit()
            flash('Profile picture updated successfully.')
            return redirect(url_for('users.profile'))

        else:
            return redirect(url_for('upload'))
    else:
        flash('UNAUTHORIZED!!')
        return render_template('users/profile.html')
