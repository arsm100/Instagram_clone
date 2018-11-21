from flask import Flask, render_template, request, redirect, url_for, flash, escape, sessions, abort
from database import db, app
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_manager, LoginManager, AnonymousUserMixin, login_url, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm, Form
from flask_wtf.csrf import CsrfProtect
from wtforms import StringField, PasswordField, SubmitField, validators


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


@app.route("/users/new")
def new():
    # if current_user
    return render_template('users/new.html')


@app.route("/users", methods=["POST"])
def create():
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password)

    new_user = User(full_name, email, username, hashed_password)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)

    return redirect(url_for('profile', user_full_name=new_user.full_name))


@app.route("/users", methods=["GET"])
@login_required
def index():
    users = User.query.all()
    return render_template('users/index.html', users=users)


@app.route("/users/<id>", methods=["GET"])
def show(id):
    user = User.query.get(id)
    return render_template('users/show.html', user=user)


# @app.route("/users/sign_in", methods=['GET'])
# def sign_in():
#     return render_template('users/sign_in.html')

def authenticate(username, password):
    try:
        user = User.query.filter_by(username=username).all()[0]
        password_check = check_password_hash(user.password, password)
        if password_check:
            return user
        else:
            flash('Wrong Username/Password!', 'Warning')
    except IndexError:
        flash('Wrong Username/Password!', 'Warning')


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField('Submit')


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


@app.route("/users/<id>/edit", methods=["GET"])
@login_required
def edit(id):
    user = User.query.get(id)
    return render_template('users/edit.html', user=user)


@app.route("/users/<id>", methods=["POST"])
@login_required
def update_or_destroy(id):
    if request.form.get('_method') == 'PUT':
        editted_user = User.query.get(id)
        editted_user.full_name = request.form.get('full_name')
        editted_user.email = request.form.get('email')
        editted_user.username = request.form.get('username')
        editted_user.password = generate_password_hash(
            request.form.get('password'))
        db.session.add(editted_user)
        db.session.commit()
        return redirect(url_for('index'))

    elif request.form.get('_method') == 'DELETE':
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
