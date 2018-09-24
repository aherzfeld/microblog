from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse  # used to redirect user to initial protected page after login 
from app import app, db  # from app package import app & db instance
from app.forms import LoginForm, RegistrationForm  # imports LoginForm class from forms.py
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


# @app.route creates an association between the URL given as an argument and the function
@app.route('/')
@app.route('/index')
@login_required  # from flask-login
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Andy'},
            'body': 'Learning Flask baby!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # from flask-login UserMixin
        return redirect(url_for('index'))
    form = LoginForm()  # instantiates form object
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # this redirects the user to the page they initially wanted to view before being prompted to login
        next_page = request.args.get('next')  # request imported from flask
        # this secures the site from attackers adding a malicious site in the next URL argument. The application only redirects when the URL is relative, and thus, only to pages with the application itself.
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)










