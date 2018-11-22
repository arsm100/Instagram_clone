from werkzeug.security import generate_password_hash
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, escape, sessions, abort
from instagram.users.models import User
from instagram.users.forms import SignupForm
from instagram import db, app, login_manager
from flask_login import login_required, login_url, current_user

users_blueprint = Blueprint(
    'users', __name__, template_folder='templates/users')


@login_manager.user_loader
def load_user(id):
    try:
        return User.query.get(id)
    except IndexError:
        pass


@users_blueprint.route("/new", methods=['GET', 'POST'])
def create():
    # if current_user.is_authenticated:
    #     flash('You must be logged out to sign up!', 'warning')
    #     return redirect(url_for('/../../../templates/home'))
    # else:
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(form.full_name.data, form.email.data,
                        form.username.data, hashed_password)
        if len(new_user.validation_errors) == 0:
            db.session.add(new_user)
            db.session.commit()
            # login_user(new_user)
            return redirect(url_for('users.profile'))
        return render_template('new.html', form=form, validation_errors=new_user.validation_errors)
    return render_template('new.html', form=form)


@users_blueprint.route("/profile")
@login_required
def profile():
    return render_template('profile.html')
