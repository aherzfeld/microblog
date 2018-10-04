from app import create_app, db, cli
from app.models import User, Post


app = create_app()
'''
workaround because current_app does not work when commands are created are
registered at start up, not during the handlin of a request which is the only
time current_app can be used. The workout around was to create a register()
function in cli.py that takes the app instance as an arg and call it here.
'''
cli.register(app)


'''
this decorator registers the function as a shell context function when the
'flask shell' command runs, it will invoke this function and register the
items returned by it in the shell session. The dictionary keys provide the
names the can be referenced by in the shell.
'''


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
