from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, escape, sessions
from instagram.sessions.forms import LoginForm
from instagram.sessions.models import authenticate
from flask_login import login_user, logout_user, login_url, login_required, current_user


sessions_blueprint = Blueprint(
    'sessions', __name__, template_folder='templates/')


@sessions_blueprint.route('/new', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate(form.username.data, form.password.data)
        if user is None:
            return redirect(url_for('sessions.login'))
        login_user(user)
        flash('Logged in successfully.')
        next = request.args.get('next')
        return redirect(next or url_for('users.profile', id=current_user.id))
    return render_template('sessions/new.html', form=form)


@sessions_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('home'))
