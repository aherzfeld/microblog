from flask import render_template, flash, redirect, url_for
from app import app  # from app package import app instance
from app.forms import LoginForm  # imports LoginForm class from forms.py


# @app.route creates an association between the URL given as an argument and the function
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Bongja'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # instantiates form object
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)














