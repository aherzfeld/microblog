from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import UserMixin  # generic implementations for the user model
from app import login  # from flask-login to be used for user loader function
from hashlib import md5  # this is used to hash emails for gravatars


# This is an auxiliary table and has no data except foreign keys, and thus, it doesn't need an associated model class.
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # this is not an actual database field, but a high-level view of the relationship between users and posts
    # the first argument to db.relationship is the model class that represents the "many" side of the relationship - in this case 'Post'
    # the backref argument defines the name of a field that will be added to the objects of the "many" class that points back at the "one" object.
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # logic to generate avatars - Part 6 - Flask Mega Tutorial
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        # see Flask-Mega Tutorial Part 8: followers
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        # we want to include a users own posts to be displayed
        own = Post.query.filter_by(user_id=self.id)
        # we union the followed posts and own before sorting
        return followed.union(own).order_by(Post.timestamp.desc())

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
