from instagram.helpers import allowed_file, S3_BUCKET, delete_photo
from instagram.images.models import upload_file_to_s3
from flask import Blueprint, render_template, request, redirect, url_for, flash, escape, sessions
from instagram.images.forms import UploadForm, EditCaptionForm, DeleteForm
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from instagram.users.models import User, S3_LOCATION
from instagram.images.models import Image
from instagram import db, super_admins
import random

images_blueprint = Blueprint(
    'images', __name__, template_folder='templates/')


@images_blueprint.route("<id>/upload_picture/<gallery>", methods=['GET'])
@login_required
def upload(id, gallery):
    form = UploadForm()
    return render_template('images/upload.html', form=form, gallery=gallery)


@images_blueprint.route("<id>/new", methods=['POST'])
@login_required
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
            serial_filename = f'{current_user.id}.{random.randint(1,1000)}.{file.filename}'
            file.filename = secure_filename(serial_filename)
            image_name = upload_file_to_s3(file, S3_BUCKET)
            if request.form.get('_folder') == 'True':
                new_image = Image(str(image_name), id, caption)
                db.session.add(new_image)
                db.session.commit()
                flash('image added to gallery successfully.')
                return redirect(url_for('users.profile', id=current_user.id))

            elif request.form.get('_folder') == 'False':
                editted_user = User.query.get(current_user.id)
                delete_photo(editted_user.profile_picture_name)
                editted_user.profile_picture_name = str(image_name)
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


@images_blueprint.route("/<id>/edit", methods=["GET"])
@login_required
def edit(id):
    editted_image = Image.query.get(id)
    if current_user.username in super_admins or editted_image.user_id == current_user.id:
        form = EditCaptionForm()
        form.image_caption.data = editted_image.image_caption
        return render_template('images/edit.html', id=id, form=form, Image=Image, S3_LOCATION=S3_LOCATION)
    else:
        flash('UNAUTHORIZED!!')
        return render_template('users/profile.html', id=current_user.id)


@images_blueprint.route("/<id>/delete", methods=["GET"])
@login_required
def delete(id):
    editted_image = Image.query.get(id)
    if current_user.username in super_admins or editted_image.user_id == current_user.id:
        form = DeleteForm()
        return render_template('images/delete.html', id=id, form=form, Image=Image, S3_LOCATION=S3_LOCATION)
    else:
        flash('UNAUTHORIZED!!')
        return render_template('users/profile.html', id=current_user.id)


@images_blueprint.route("/<id>/update", methods=["POST"])
@login_required
def update_or_destroy(id):
    if request.form.get('_method') == 'PUT':
        form = EditCaptionForm()
        if form.validate_on_submit():
            editted_image = Image.query.get(id)
            editted_image.image_caption = form.image_caption.data
            db.session.add(editted_image)
            db.session.commit()
            flash('Image caption updated successfully.')
            return redirect(url_for('users.profile', id=current_user.id))
        return render_template('images/edit.html', id=id, form=form, Image=Image, S3_LOCATION=S3_LOCATION)
    if request.form.get('_method') == 'DELETE':
        form = DeleteForm()
        if form.validate_on_submit():
            deleted_image = Image.query.get(id)
            delete_photo(deleted_image.image_name)
            db.session.delete(deleted_image)
            db.session.commit()
            flash('Image deleted successfully.')
            return redirect(url_for('home'))
        return render_template('images/delete.html', id=id, form=form, Image=Image, S3_LOCATION=S3_LOCATION)
