from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, escape, sessions, abort
from jinja2 import TemplateNotFound
from instagram import app, db
from instagram.users.models import User
from werkzeug.security import generate_password_hash
from flask_login import login_manager, LoginManager, AnonymousUserMixin, login_url, login_user, logout_user, login_required, current_user


@app.route("/")
def home():
    user_full_name = request.args.get('user_full_name')
    return render_template('home.html', user_full_name=user_full_name)


if __name__ == '__main__':
    app.run()
