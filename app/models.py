from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # this is not an actual database field, but a high-level view of the relationship between users and posts
    # the first argument to db.relationship is the model class that represents the "many" side of the relationship - in this case 'Post'
    # the backref argument defines the name of a field that will be added to the objects of the "many" class that points back at the "one" object.
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # timestamp is indexed, which is useful to retreive posts in chrono order
    # also note, that we passed the datetime function iteself - without the () - not the result of calling it
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # initialized as a foreign key which references an id value from the user table
    # 'user.id' is the database table name - that's why its lowercase
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
