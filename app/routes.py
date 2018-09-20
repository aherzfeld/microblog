from flask import render_template
from app import app  # from app package import app instance


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
