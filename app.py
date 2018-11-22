from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, escape, sessions, abort
from jinja2 import TemplateNotFound
from instagram import app, db
from instagram.users.models import User
from werkzeug.security import generate_password_hash
from flask_login import login_manager, LoginManager, AnonymousUserMixin, login_url, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, validators
from forms import LoginForm, EditForm, DeleteForm


@app.route("/")
def home():
    user_full_name = request.args.get('user_full_name')
    return render_template('home.html', user_full_name=user_full_name)


# @app.route("/users/profile")
# @login_required
# def profile():
#     user_full_name = request.args.get('user_full_name')
#     return render_template('users/profile.html', user_full_name=user_full_name)


@app.route("/users", methods=["GET"])
@login_required
def index():
    users = User.query.all()
    return render_template('users/index.html', users=users)


@app.route("/users/<id>", methods=["GET"])
def show(id):
    user = User.query.get(id)
    return render_template('users/show.html', user=user)


@app.route("/settings")
@login_required
def settings():
    return '<h1>Settings Page</h1>'


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('home'))


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
