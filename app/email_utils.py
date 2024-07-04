from threading import Thread
from flask import current_app


def send_async_email(app, msg):
    """

    :param app:
    :param msg:
    """
    with app.app_context():
        app.extensions['mail'].send(msg)


def send_email_in_background(app, msg):
    """

    :param app:
    :param msg:
    """
    Thread(target=send_async_email, args=(app, msg)).start()
