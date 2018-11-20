from flask import Flask, render_template, request, redirect, url_for, flash, escape, sessions
from database import db, app
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_manager, LoginManager, UserMixin, AnonymousUserMixin, login_url

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def home():
    user_full_name = request.args.get('user_full_name')
    signed_in = request.args.get('signed_in')
    return render_template('home.html', signed_in=signed_in, user_full_name=user_full_name)


@app.route("/users/profile")
def profile():
    user_full_name = request.args.get('user_full_name')
    return render_template('users/profile.html', user_full_name=user_full_name)


@app.route("/users/new")
def new():
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

    return redirect(url_for('home', user_full_name=new_user.full_name))


@app.route("/users", methods=["GET"])
def index():
    users = User.query.all()
    return render_template('users/index.html', users=users)


@app.route("/users/<id>", methods=["GET"])
def show(id):
    user = User.query.get(id)
    return render_template('users/show.html', user=user)


@app.route("/users/sign_in", methods=['GET'])
def sign_in():
    return render_template('users/sign_in.html')


@app.route("/users/sign_in", methods=["POST"])
def authenticate():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username)
    try:
        password_check = check_password_hash(user.all()[0].password, password)
        if password_check:
            flash('Welcome to Instgram Clone!', 'info')
            return redirect(url_for('profile', signed_in=True, user_full_name=user.all()[0].full_name))
        else:
            flash('Wrong Password!', 'Warning')
            return redirect(url_for('home', signed_in=False))
    except IndexError:
        flash('User doesn\'t exist!', 'Warning')
        return redirect(url_for('home', signed_in=False))


@app.route("/users/<id>/edit", methods=["GET"])
def edit(id):
    user = User.query.get(id)
    return render_template('users/edit.html', user=user)


@app.route("/users/<id>", methods=["POST"])
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
