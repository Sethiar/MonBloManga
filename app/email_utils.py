"""
Code permettant d'envoyer des mails en arrière-plan.
"""
from threading import Thread


def send_async_email(app, msg):
    """
    Envoie un email de manière asynchrone en utilisant le contexte de l'application Flask.

    Args:
        app (Flask): L'instance de l'application Flask.
        msg (Message): L'objet Message contenant les détails de l'email à envoyer.
    """
    with app.app_context():
        app.extensions['mail'].send(msg)


def send_email_in_background(app, msg):
    """
    Lance l'envoi d'un email dans un thread séparé.

    Args:
        app (Flask): L'instance de l'application Flask.
        msg (Message): L'objet Message contenant les détails de l'email à envoyer.
    """
    Thread(target=send_async_email, args=(app, msg)).start()
