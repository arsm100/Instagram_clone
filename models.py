from database import db


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.Text)
    email = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Text)

    def __init__(self, full_name, email, username, password):
        self.full_name = full_name
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User {self.full_name} has email {self.email} and username {self.username}"
