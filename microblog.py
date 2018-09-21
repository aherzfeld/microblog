from app import app, db # imports the app variable that is a member of the app package
from app.models import User, Post


# this decorator registers the function as a shell context function
# when the 'flask shell' command runs, it will invoke this function and register the items returned by it in the shell session
# the dictionary keys provide the names the can be referenced by in the shell.
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
