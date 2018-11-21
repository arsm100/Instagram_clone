from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, escape, sessions, abort
from jinja2 import TemplateNotFound
from database import db, app
from models import User, authenticate
from werkzeug.security import generate_password_hash
from flask_login import login_manager, LoginManager, AnonymousUserMixin, login_url, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm, Form
from flask_wtf.csrf import CsrfProtect
from wtforms import StringField, PasswordField, SubmitField, validators
from forms import LoginForm, SignupForm, EditForm, DeleteForm


login_manager = LoginManager()
login_manager.init_app(app)
csrf = CsrfProtect(app)
login_manager.session_protection = "basic"
login_manager.login_message = "Please login to Ahmed's Instagram first."
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(username):
    try:
        return User.query.filter_by(username=username).all()[0]
    except IndexError:
        pass


@app.route("/")
def home():
    user_full_name = request.args.get('user_full_name')
    signed_in = request.args.get('signed_in')
    return render_template('home.html', signed_in=signed_in, user_full_name=user_full_name)


@app.route("/users/profile")
@login_required
def profile():
    user_full_name = request.args.get('user_full_name')
    return render_template('users/profile.html', user_full_name=user_full_name)


@app.route("/users/new", methods=['GET', 'POST'])
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
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('profile'))
        return render_template('users/new.html', form=form)


@app.route("/users", methods=["GET"])
@login_required
def index():
    users = User.query.all()
    return render_template('users/index.html', users=users)


@app.route("/users/<id>", methods=["GET"])
def show(id):
    user = User.query.get(id)
    return render_template('users/show.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate(form.username.data, form.password.data)
        if user is None:
            return redirect(url_for('login'))
        login_user(user)
        flash('Logged in successfully.')
        next = request.args.get('next')
        return redirect(next or url_for('profile'))
    return render_template('login.html', form=form)


@app.route("/settings")
@login_required
def settings():
    return '<h1>Settings Page</h1>'


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# @app.route("/users/<id>/edit", methods=["GET"])
# @login_required
# def edit(id):
#     user = User.query.get(id)
#     return render_template('users/edit.html', user=user)


@app.route("/users/<id>/edit", methods=["GET", "POST"])
@login_required
def update_or_destroy(id):
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
            next = request.args.get('next')
            return redirect(next or url_for('profile'))
        return render_template('users/edit.html', User=User, id=id, form=form)
    if request.args.get('_method') == 'DELETE':
        form = DeleteForm()
        return render_template('users/delete.html', id=id, form=form)
    if request.form.get('_method') == 'DELETE':
        form = DeleteForm()
        if form.validate_on_submit():
            user = User.query.get(id)
            logout_user()
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('users/delete.html', id=id, form=form)


if __name__ == '__main__':
    app.run()
