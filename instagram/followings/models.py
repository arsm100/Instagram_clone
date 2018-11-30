from instagram import db


class Users_Users(db.Model):

    __tablename__ = 'users_users'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), index=True, nullable=False)
    followed_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), index=True, nullable=False)
    follower = db.relationship("User", foreign_keys=[
                               follower_id], back_populates="followers")
    following = db.relationship("User", foreign_keys=[
        followed_id], back_populates="following")

    def __init__(self, follower_id, followed_id):
        self.follower_id = follower_id
        self.followed_id = followed_id

    def __repr__(self):
        return f"User {self.follower_id} has followed user {self.followed_id}"
