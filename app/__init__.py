from flask import Flask  # imports Flask object from flask package
from config import Config  # imports Config class from config.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging  # python's logging package - can send logs by email
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__)  # creates app object as instance of class Flask
app.config.from_object(Config)
db = SQLAlchemy(app)  # instantiate db by passing the app to SQLAlchemy
migrate = Migrate(app, db)  # also instantiate the database migration engine
login = LoginManager(app)  # instantiates flask-login
login.login_view = 'login'  # this tells flask-login which view function handles logins

# this app package is defined by the app directory and the __init__.py script
# imported below app instantiation to avoid circular imports
from app import routes, models, errors  

# email logger only enabled when not in debug mode
if not app.debug:
    # also only enabled when email server exists in configuration
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        # creates SMTPHandler instance & sets it to only report errors
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        # attaches SMTPHandler instance to the app.logger object from Flask
        app.logger.addHandler(mail_handler)
    if not os.path.exists('logs'):
        os.mkdir('logs')
    # rotates logs to new file once they reach 10KB - 10 files total
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    # provides custom formatting for log messages
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    # Sets logging level to INFO
    # categories in increasing severity: DEBUG, INFO, WARNING, ERROR, CRITICAL
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')






