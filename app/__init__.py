from flask import Flask  # imports Flask object from flask package

app = Flask(__name__)  # creates app object as instance of class Flask

# this app package is defined by the app directory and the __init__.py script
# imported below app instantiation to avoid circular imports
from app import routes  
