from flask import render_template, request, redirect, url_for, flash
from database import db, app
from models import Puppy


@app.route("/")
def home():
    puppy_name = request.args.get('puppy_name')
    return render_template('home.html', puppy_name=puppy_name)


@app.route("/puppies/new")
def new():
    return render_template('puppies/new.html')


@app.route("/puppies", methods=["POST"])
def create():
    name = request.form.get('name')
    age = request.form.get('age')
    breed = request.form.get('breed')

    new_puppy = Puppy(name, age, breed)
    db.session.add(new_puppy)
    db.session.commit()

    return redirect(url_for('home', puppy_name=new_puppy.name))


@app.route("/puppies", methods=["GET"])
def index():
    puppies = Puppy.query.all()
    return render_template('puppies/index.html', puppies=puppies)


@app.route("/puppies/<id>", methods=["GET"])
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
