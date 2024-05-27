"""
Code permettant de définir les routes concernant le mailing du blog.
"""

from app.mail import mail_bp
from flask import current_app as app, redirect, url_for, flash
from flask_mail import Message
from Models.user import User
from Models import db, user
from datetime import date


@mail_bp.route("/send_mail")
def send_email():
    """
    Envoie un e-mail de test.

    Cette route envoie un e-mail de test à une adresse prédéfinie pour vérifier que
    la configuration de Flask-Mail fonctionne correctement.

    :return: Un message indiquant que l'e-mail a été envoyé avec succès.
    """
    mail = app.extensions['mail']
    msg = Message("Hello",
                  sender="alefetey123@gmail.com",
                  recipients=["alefetey123@gmail.com"])
    msg.body = "ce mail est un mail test permettant de vérifier le fonctionnement du serveur smtp."
    mail.send(msg)
    return "Email envoyé !"


@mail_bp.route("/send_confirmation_email/<string:email>")
def send_confirmation_email(email):
    """
    Envoie un e-mail de confirmation d'inscription à un nouvel utilisateur.

    Cette route envoie un e-mail de confirmation à l'adresse e-mail fournie
    après l'inscription d'un nouvel utilisateur.

    :param email: L'adresse e-mail du nouvel utilisateur.
    :return: Une redirection vers la page d'accueil après envoi de l'e-mail de confirmation.
    """
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Utilisateur non trouvé.", "Attention")
        return redirect(url_for('landing_page'))

    mail = app.extensions['mail']
    msg = Message("Confirmation d'inscription", sender='alefetey123@gmail.com', recipients=[email])
    msg.body = "Merci de vous être inscrit sur notre site. Votre inscription a été confirmée avec succès.\n" \
               "Nous espérons que nous vous retrouverons bientôt afin d'entendre votre voix sur notre blog.\n" \
            f"Merci {user.pseudo} de votre confiance."
    mail.send(msg)
    return redirect(url_for("landing_page"))


def mail_birthday():
    """
    Envoie des e-mails de souhaits d'anniversaire aux utilisateurs.

    Cette fonction vérifie les dates de naissance des utilisateurs dans la base de données
    et envoie un e-mail de souhaits d'anniversaire à ceux dont l'anniversaire est aujourd'hui.
    """
    today = date.today()
    users = User.query.filter(db.extract('month', User.date_naissance) == today.month,
                              db.extract('day', User.date_naissance) == today.day).all()
    for user in users:
        send_birthday_email(user)


def send_birthday_email(user):
    """
    Envoie un e-mail de souhaits d'anniversaire à un utilisateur.

    Cette fonction envoie un e-mail de souhaits d'anniversaire à l'utilisateur
    fourni en paramètre.

    :param user: L'utilisateur à qui envoyer l'e-mail de souhaits d'anniversaire.
    """
    mail = app.extensions['mail']
    msg = Message("Joyeux anniversaire !",
                  sender='alefetey123@gmail.com',
                  recipients=[user.email])
    msg.body = f"Bonjour {user.email},\n\nNous vous souhaitons un très joyeux anniversaire !\n\nCordialement,\nL'équipe du blog."
    mail.send(msg)

