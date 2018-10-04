from threading import Thread  # for sending asynchronous emails
from flask import current_app
from flask_mail import Message
from app import mail


'''runs in a background thread, invoked via the Thread() class in the last
line of send_email()'''


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object, msg)).start()
"""
Using current_app directly in the send_async_email() function that runs as a
background thread would not have worked , because current_app is a context-
aware variable that is tied to the thread that is handling the client request.
We need to access the real application instance that is stored inside the proxy
object, and pass that as the app arg. the current_app._get_current_object() 
does just that. So that is what we pass to the thread as an arg.
"""