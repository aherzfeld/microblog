from threading import Thread  # for sending asynchronous emails
from flask import render_template
from flask_mail import Message
from flask_babel import _  # function call to mark text for translation
from app import app, mail



'''runs in a background thread, invoked via the Thread() class in the last
line of send_email()'''
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    # email subject wrapped in babel text marking function
    send_email(_('[Microblog] Reset Your Password'),
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
