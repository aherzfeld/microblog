from flask import Flask  # imports Flask object from flask package
from config import Config  # imports Config class from config.py

app = Flask(__name__)  # creates app object as instance of class Flask
app.config.from_object(Config)

# this app package is defined by the app directory and the __init__.py script
# imported below app instantiation to avoid circular imports
from app import routes  
