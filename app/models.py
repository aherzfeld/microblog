from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import UserMixin  # generic implementations for the user model
from app import login  # from flask-login to be used for user loader function


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # this is not an actual database field, but a high-level view of the relationship between users and posts
    # the first argument to db.relationship is the model class that represents the "many" side of the relationship - in this case 'Post'
    # the backref argument defines the name of a field that will be added to the objects of the "many" class that points back at the "one" object.
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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


# user loader function to help flask-login load a user from the db
# flask-login passes the id as a string so it needs to be converted for the db
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
