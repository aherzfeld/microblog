from flask import Flask  # imports Flask object from flask package
from config import Config  # imports Config class from config.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)  # creates app object as instance of class Flask
app.config.from_object(Config)
db = SQLAlchemy(app)  # instantiate db by passing the app to SQLAlchemy
migrate = Migrate(app, db)  # also instantiate the database migration engine

# this app package is defined by the app directory and the __init__.py script
# imported below app instantiation to avoid circular imports
from app import routes, models  
