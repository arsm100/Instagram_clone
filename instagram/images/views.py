from instagram.helpers import allowed_file, S3_BUCKET
from instagram.images.models import upload_file_to_s3
from flask import Blueprint, render_template, request, redirect, url_for, flash, escape, sessions
from instagram.images.forms import UploadForm
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from instagram.users.models import User, S3_LOCATION
from instagram.images.models import Image
from instagram import db, super_admins


images_blueprint = Blueprint(
    'images', __name__, template_folder='templates/')


@images_blueprint.route("<id>/upload_picture/<gallery>", methods=['GET'])
def upload(id, gallery):
    form = UploadForm()
    return render_template('images/upload.html', form=form, gallery=gallery)


@images_blueprint.route("<id>/new", methods=['POST'])
def upload_image(id):
    if current_user.username in super_admins or int(id) == current_user.id:

            # check there is a file
        if "user_photo" not in request.files:
            flash("No photo was uploaded")
            return redirect(url_for('images.upload', id=current_user.id))

            # grab the photo and caption
        file = request.files["user_photo"]
        caption = request.form["image_caption"]

        # check there is a name
        if file.filename == "":
            flash("Please give your photo a valid name!")
            return redirect(url_for('images.upload', id=current_user.id))

            # check correct extension and upload if valid
        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)
            output = upload_file_to_s3(file, S3_BUCKET)
            if request.form.get('_folder') == 'True':
                new_image = Image(str(output), id, caption)
                db.session.add(new_image)
                db.session.commit()
                flash('image added to gallery successfully.')
                return redirect(url_for('users.profile', id=current_user.id))

            elif request.form.get('_folder') == 'False':
                editted_user = User.query.get(current_user.id)
                editted_user.profile_picture_name = str(output)
                db.session.add(editted_user)
                db.session.commit()
                flash('Profile picture updated successfully.')
                return redirect(url_for('users.profile', id=current_user.id))

        else:
            flash('Please upload a valid photo file!')
            return redirect(url_for('images.upload', id=current_user.id))
    else:
        flash('UNAUTHORIZED!!')
        return render_template('users/profile.html', id=current_user.id)


@images_blueprint.route("/", methods=["GET"])
@login_required
def index():
    if current_user.username in super_admins:
        images = Image.query.all()
        return render_template('images/index.html', S3_LOCATION=S3_LOCATION, images=images)
    flash('UNAUTHORIZED!!')
    return render_template('users/profile.html', id=current_user.id)
