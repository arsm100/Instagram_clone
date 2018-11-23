from werkzeug.security import generate_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash, escape, sessions
from instagram.users.models import User
from instagram.users.forms import SignupForm, EditForm, DeleteForm
from instagram import db, login_manager
from flask_login import login_user, logout_user, login_required, login_url, current_user

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
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(form.full_name.data, form.email.data,
                            form.username.data, hashed_password)
            if len(new_user.validation_errors) == 0:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('users.profile'))
            return render_template('users/new.html', form=form, validation_errors=new_user.validation_errors)
        return render_template('users/new.html', form=form)


@users_blueprint.route("/profile")
@login_required
def profile():
    return render_template('users/profile.html')


@users_blueprint.route("/<id>", methods=["GET"])
@login_required
def show(id):
    if current_user.username in ('ahmedramzy160', 'josh777') or int(id) == current_user.id:
        user = User.query.get(id)
        return render_template('users/show.html', user=user)
    else:
        flash('UNAUTHORIZED!!')
        return render_template('users/profile.html')


@users_blueprint.route("/", methods=["GET"])
@login_required
def index():
    if current_user.username in ('ahmedramzy160', 'josh777'):
        users = User.query.all()
        return render_template('users/index.html', users=users)
    flash('UNAUTHORIZED!!')
    return render_template('users/profile.html')


@users_blueprint.route("/<id>/settings")
@login_required
def settings(id):
    return f'<h1>{id} Settings Page</h1>'


@users_blueprint.route("/<id>/edit", methods=["GET", "POST"])
@login_required
def update_or_destroy(id):
    if current_user.username in ('ahmedramzy160', 'josh777') or int(id) == current_user.id:
        if request.args.get('_method') == 'PUT':
            form = EditForm()
            return render_template('users/edit.html', User=User, id=id, form=form)
        if request.form.get('_method') == 'PUT':
            form = EditForm()
            if form.validate_on_submit():
                editted_user = User.query.get(id)
                editted_user.full_name = form.full_name.data
                editted_user.email = form.email.data
                editted_user.username = form.username.data
                editted_user.password = generate_password_hash(
                    form.password.data)
                db.session.add(editted_user)
                db.session.commit()
                flash('User details updated successfully.')
                return redirect(url_for('users.profile'))
            return render_template('users/edit.html', User=User, id=id, form=form)
        if request.args.get('_method') == 'DELETE':
            form = DeleteForm()
            return render_template('users/delete.html', id=id, form=form)
        if request.form.get('_method') == 'DELETE':
            form = DeleteForm()
            if form.validate_on_submit():
                user = User.query.get(id)
                if int(id) == current_user.id:
                    logout_user()
                db.session.delete(user)
                db.session.commit()
                flash('User deleted successfully.')
                return redirect(url_for('home'))
            return render_template('users/delete.html', id=id, form=form)
    else:
        flash('UNAUTHORIZED!!')
        return render_template('users/profile.html')
