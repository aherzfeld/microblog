from app import app  # from app package import app instance


# @app.route creates an association between the URL given as an argument and the function
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
    