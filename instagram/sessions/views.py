from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, escape, sessions
from instagram.sessions.forms import LoginForm
from instagram.sessions.models import authenticate
from instagram.users.models import User
from flask_login import login_user, logout_user, login_url, login_required, current_user
from instagram import oauth, google, REDIRECT_URI


sessions_blueprint = Blueprint(
    'sessions', __name__, template_folder='templates/')


@sessions_blueprint.route('/check/google')
def google_authorize():
    redirect_uri = url_for(REDIRECT_URI, _external=True)
    return google.authorize_redirect(redirect_uri)


@sessions_blueprint.route('/authorize/google')
def google_authorize_login():
    token = oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    # full_name = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['name']
    user = User.query.filter_by(email=email).first()
    if user:
        login_user(user)
        return redirect(url_for('users.profile', id=user.id))
    else:
        flash('You haven\'t signed up for an Aragram account yet! Please fill this signup form to create an account')
        return redirect(url_for('users.create'))


@sessions_blueprint.route('/new', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate(form.username.data, form.password.data)
        if user is None:
            return render_template('sessions/new.html', form=form)
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
