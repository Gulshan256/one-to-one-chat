from settings import db,app
from datetime import datetime
from passlib.hash import pbkdf2_sha256



# class Client(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     password = db.Column(db.String(100), nullable=False)

class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    friends = db.relationship(
        'User',
        secondary='friendship',
        primaryjoin=(id == Friendship.user_id),
        secondaryjoin=(id == Friendship.friend_id),
        backref=db.backref('friendship', lazy='dynamic'),
        lazy='dynamic',
        foreign_keys=[Friendship.user_id, Friendship.friend_id]
    )



    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        # decoded_password = base64.b64decode(password)
        return pbkdf2_sha256.verify(password, self.password)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message_text = db.Column(db.String(1000), nullable=False)
    sent_time = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id])
    recipient = db.relationship('User', foreign_keys=[recipient_id])



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        