from instagram import db


class Donation(db.Model):

    __tablename__ = 'donations'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey(
        'images.id'), nullable=False)
    amount = db.Column(db.Numeric(), nullable=False)
    currency = db.Column(db.String(3), nullable=False, default='USD')
    donor = db.relationship("User", foreign_keys=[
                            sender_id], back_populates="donations_out")
    receiver = db.relationship("User", foreign_keys=[
                               receiver_id], back_populates="donations_in")

    def __init__(self, sender_id, receiver_id, image_id, amount, currency='USD'):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.image_id = image_id
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"Donation of {self.amount} has been made to {self.receiver_id} by {self.sender_id} for {self.image_id}"


class Users_Users(db.Model):

    __tablename__ = 'users_users'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    followed_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    follower = db.relationship("User", foreign_keys=[
                               follower_id], back_populates="followers")
    following = db.relationship("User", foreign_keys=[
        followed_id], back_populates="following")

    def __init__(self, follower_id, followed_id):
        self.follower_id = follower_id
        self.followed_id = followed_id

    def __repr__(self):
        return f"User {self.follower_id} has followed user {self.followed_id}"
