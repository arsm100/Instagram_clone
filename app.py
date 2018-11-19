from flask import render_template, request, redirect, url_for, flash
from database import db, app
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_manager, LoginManager


@app.route("/")
def home():
    user_full_name = request.args.get('user_full_name')
    return render_template('home.html', user_full_name=user_full_name)


@app.route("/users/new")
def new():
    return render_template('users/new.html')


@app.route("/users", methods=["POST"])
def create():
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    new_user = User(full_name, email, username, password)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('home', user_full_name=new_user.full_name))


@app.route("/users", methods=["GET"])
def index():
    users = User.query.all()
    return render_template('users/index.html', users=users)


@app.route("/users/<id>", methods=["GET"])
def show(id):
    puppy = Puppy.query.get(id)
    return render_template('puppies/show.html', puppy=puppy)


@app.route("/puppies/<id>/edit", methods=["GET"])
def edit(id):
    puppy = Puppy.query.get(id)
    return render_template('puppies/edit.html', puppy=puppy)


@app.route("/puppies/<id>", methods=["POST"])
def update_or_destroy(id):
    if request.form.get('_method') == 'PUT':
        editted_puppy = Puppy.query.get(id)
        editted_puppy.name = request.form.get('name')
        editted_puppy.age = request.form.get('age')
        editted_puppy.breed = request.form.get('breed')
        db.session.add(editted_puppy)
        db.session.commit()
        return redirect(url_for('home', puppy_name=editted_puppy.name))
    elif request.form.get('_method') == 'DELETE':
        pup = Puppy.query.get(id)
        db.session.delete(pup)
        db.session.commit()
        return redirect(url_for('index', puppy_name=pup.name))


if __name__ == '__main__':
    app.run()
