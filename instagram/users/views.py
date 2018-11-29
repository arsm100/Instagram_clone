# from flask_mail import Mail, Message
from flask import Blueprint, render_template, request, redirect, url_for, flash, escape, sessions
from instagram.users.models import User
from instagram.images.models import Image
from instagram.users.forms import SignupForm, EditForm, DeleteForm, SearchForm
from instagram import db, login_manager, super_admins, S3_LOCATION
from flask_login import login_user, logout_user, login_required, login_url, current_user
from instagram.helpers import delete_photo, send_signup_email

users_blueprint = Blueprint(
    'users', __name__, template_folder='templates/')


@login_manager.user_loader
def load_user(id):
    try:
        return User.query.get(id)
    except IndexError:
        pass


@users_blueprint.route("/new", methods=['GET', 'POST'])
def create():
    if current_user.is_authenticated:
        flash('You must be logged out to sign up!', 'warning')
        return redirect(url_for('home'))
    else:
        form = SignupForm()
        if form.validate_on_submit():
            new_user = User(form.full_name.data, form.email.data,
                            form.username.data.lower(), form.password.data)
            if len(new_user.validation_errors) == 0:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                send_signup_email(new_user.email)
                return redirect(url_for('users.profile', User=User, id=current_user.id))
            return render_template('users/new.html', form=form, validation_errors=new_user.validation_errors)
        return render_template('users/new.html', form=form)


@users_blueprint.route("<id>/profile")
@login_required
def profile(id):
    user = User.query.get(id)
    if not user.is_private or current_user.username in super_admins or int(id) == current_user.id:
        return render_template('users/profile.html', User=User, id=int(id), S3_LOCATION=S3_LOCATION)
    else:
        flash('No public accounts found!')
        return render_template('users/profile.html', User=User, id=current_user.id, S3_LOCATION=S3_LOCATION)


@users_blueprint.route("/<id>", methods=["GET"])
@login_required
def show(id):
    if current_user.username in super_admins or int(id) == current_user.id:
        user = User.query.get(id)
        return render_template('users/show.html', user=user)
    else:
        flash('UNAUTHORIZED!!')
        return render_template('users/profile.html', id=id)


@users_blueprint.route("/", methods=["GET"])
@login_required
def index():
    if current_user.username in super_admins:
        users = User.query.all()
        return render_template('users/index.html', users=users)
    flash('UNAUTHORIZED!!')
    return render_template('users/profile.html', id=current_user.id)


@users_blueprint.route("/<id>/settings")
@login_required
def settings(id):
    return f'<h1>{id} Settings Page</h1>'


@users_blueprint.route("/<id>/edit", methods=["GET"])
@login_required
def edit(id):
    editted_user = User.query.get(id)
    if current_user.username in super_admins or int(id) == current_user.id:
        form = EditForm()
        form.full_name.data = editted_user.full_name
        form.email.data = editted_user.email
        form.username.data = editted_user.username
        form.password.data = editted_user.password
        return render_template('users/edit.html', id=id, form=form)
    else:
        flash('UNAUTHORIZED!!')
        return render_template('users/profile.html', id=id)


@users_blueprint.route("/<id>/delete", methods=["GET"])
@login_required
def delete(id):
    if current_user.username in super_admins or int(id) == current_user.id:
        form = DeleteForm()
        return render_template('users/delete.html', id=id, form=form, User=User)
    else:
        flash('UNAUTHORIZED!!')
        return render_template('users/profile.html', id=id)


@users_blueprint.route("/<id>/update", methods=["POST"])
@login_required
def update_or_destroy(id):
    if request.form.get('_method') == 'PUT':
        form = EditForm()
        if form.validate_on_submit():
            editted_user = User.query.get(id)
            editted_user.full_name = form.full_name.data
            editted_user.email = form.email.data
            editted_user.username = form.username.data
            editted_user.password = form.password.data
            if len(editted_user.validation_errors) == 0:
                db.session.add(editted_user)
                db.session.commit()
                flash('User details updated successfully')
                return redirect(url_for('users.profile', id=id))
            return render_template('users/edit.html', id=id, form=form, validation_errors=editted_user.validation_errors)
        return render_template('users/edit.html', id=id, form=form)
    if request.form.get('_method') == 'DELETE':
        form = DeleteForm()
        if form.validate_on_submit():
            user = User.query.get(id)
            if int(id) == current_user.id:
                logout_user()
            for image in user.images:
                delete_photo(image.image_name)
                db.session.delete(image)
                db.session.commit()
            db.session.delete(user)
            db.session.commit()
            flash('User deleted successfully')
            return redirect(url_for('home'))
        return render_template('users/delete.html', id=id, form=form, User=User)


@users_blueprint.route("/<id>/change_privacy")
@login_required
def change_privacy(id):
    if current_user.username in super_admins or int(id) == current_user.id:
        user_editting_privacy = User.query.get(id)
        user_editting_privacy.is_private = not user_editting_privacy.is_private
        db.session.add(user_editting_privacy)
        db.session.commit()
        flash('User privacy updated successfully')
        return redirect(request.referrer or url_for('users.profile', id=id))


@users_blueprint.route("/search")
def search():
    query = request.args['query']
    user = User.query.filter(User.username.like(f'{query}%')).first()
    if user:
        return redirect(url_for('users.profile', id=user.id))
    user = User.query.filter(User.email.like(f'{query}%')).first()
    if user:
        return redirect(url_for('users.profile', id=user.id))
    else:
        flash('User doesn\'t exist!')
        return redirect(url_for('users.profile', id=current_user.id))
