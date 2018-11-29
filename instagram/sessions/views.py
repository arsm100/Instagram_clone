from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, escape, sessions
from instagram.sessions.forms import LoginForm
from instagram.sessions.models import authenticate
from instagram.users.models import User
from flask_login import login_user, logout_user, login_url, login_required, current_user
from instagram import oauth, google, REDIRECT_URI, REDIRECT_URI_NEW,db
from instagram.helpers import send_signup_email
import random


sessions_blueprint = Blueprint(
    'sessions', __name__, template_folder='templates/')


@sessions_blueprint.route('/check/google')
def google_authorize():
    redirect_uri = url_for(REDIRECT_URI, _external=True)
    return google.authorize_redirect(redirect_uri)


@sessions_blueprint.route('/use/google')
def google_new():
    redirect_uri = url_for(REDIRECT_URI_NEW, _external=True)
    return google.authorize_redirect(redirect_uri)


@sessions_blueprint.route('/create/google')
def google_new_create():
    token = oauth.google.authorize_access_token()
    email = oauth.google.get(
        'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    full_name = oauth.google.get(
        'https://www.googleapis.com/oauth2/v2/userinfo').json()['name']
    given_name = oauth.google.get(
        'https://www.googleapis.com/oauth2/v2/userinfo').json()['given_name']
    new_user = User(full_name, email, f'{given_name.lower()}{random.randint(1,1000)}', str(random.randint(
        10000000, 99999999)))
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    flash('Aragram account created successfully!')
    flash('Please create a password for your Aragram account from the Edit your details option under the Settings tab')
    send_signup_email(new_user.email)
    return redirect(url_for('users.profile', User=User, id=current_user.id))


@sessions_blueprint.route('/authorize/google')
def google_authorize_login():
    token = oauth.google.authorize_access_token()
    email = oauth.google.get(
        'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.query.filter_by(email=email).first()
    if user:
        login_user(user)
        return redirect(url_for('users.profile', id=user.id))
    else:
        flash('You haven\'t signed up for an Aragram account yet! Don\'t worry though, you can create an Aragram account using your google account!')
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
