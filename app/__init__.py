import logging  # python's logging package - can send logs by email
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment  # to work with moment.js for datetimes
from flask_babel import Babel, lazy_gettext as _l  # translation extension
from config import Config  # imports Config class from config.py


# these create extension instances that are not attached to the app
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
# this tells flask-login which view function handles logins
login.login_view = 'auth.login'
# we created a custom message for babel to use for translation
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


# app factory function
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # the init_app() method binds the extensions to the now known app
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    # import of blueprint here to avoid circular dependencies
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    # the url_prefix is optional - any routes defined in this bp will get this prefix in their URLs. Useful for namespacing
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # email logger only enabled when not in debug or testing mode
    if not app.debug and not app.testing:
        # also only enabled when email server exists in configuration
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
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

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            # rotates logs to new file once they reach 10KB - 10 files total
            file_handler = RotatingFileHandler('logs/microblog.log',
                                               maxBytes=10240, backupCount=10)
            # provides custom formatting for log messages
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            # Sets logging level to INFO
            # categories in increasing severity: DEBUG, INFO, WARNING, ERROR, CRITICAL
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app

# using attribute of Flask's request object - accept_languages
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


# this app package is defined by the app directory and the __init__.py script
# imported below app instantiation to avoid circular imports
from app import models

