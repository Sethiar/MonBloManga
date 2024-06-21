"""
Code permettant de définir les routes concernant le mailing du blog.
"""

from app.mail import mail_bp

from flask import redirect, url_for, flash, current_app

from flask_mail import Message

from app.Models.user import User
from app.Models import db


from datetime import date


@mail_bp.route("/send_mail")
def send_email():
    """
    Envoie un e-mail de test à une adresse prédéfinie pour vérifier la configuration de Flask-Mail.

    Returns :
        str: Message indiquant que l'e-mail a été envoyé avec succès.
    """
    mail = current_app.extensions['mail']
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

    Args :
        email (str) : L'adresse e-mail du nouvel utilisateur.

    Returns :
        flask.Response : Redirection vers la page d'accueil après envoi de l'e-mail de confirmation.
    """
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Utilisateur non trouvé.", "Attention")
        return redirect(url_for('landing_page'))

    mail = current_app.extensions['mail']
    msg = Message("Confirmation d'inscription", sender='alefetey123@gmail.com', recipients=[email])
    msg.body = "Merci de vous être inscrit sur notre site. Votre inscription a été confirmée avec succès.\n" \
               "Nous espérons que nous vous retrouverons bientôt afin d'entendre votre voix sur notre blog.\n" \
            f"Merci {user.pseudo} de votre confiance."
    mail.send(msg)


def mail_birthday():
    """
    Envoie des e-mails de souhaits d'anniversaire aux utilisateurs dont c'est l'anniversaire aujourd'hui.

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
    Envoie un e-mail de souhaits d'anniversaire à un utilisateur spécifique.

    Args:
        user (User): L'utilisateur à qui envoyer l'e-mail de souhaits d'anniversaire.
    """
    mail = current_app.extensions['mail']
    msg = Message("Joyeux anniversaire !",
                  sender='alefetey123@gmail.com',
                  recipients=[user.email])
    msg.body = f"Bonjour {user.email},\n\nNous vous souhaitons un très joyeux anniversaire !\n" \
               f"\nCordialement,\nL'équipe du blog."
    mail.send(msg)


def mail_banned_user(user):
    """
    Envoie un e-mail informant un utilisateur de son bannissement temporaire pour non-respect des règles.

    Args:
        user (User): L'utilisateur qui sera banni.
    """
    mail = current_app.extensions['mail']
    msg = Message("Bannissement",
                  sender='alefetey123@gmail.com',
                  recipients=[user.email])
    msg.body = f"Bonjour {user.pseudo}," \
               f"Suite à la tenue des règles en vigueur sur le blog, {user.pseudo}, vous avez été banni " \
               f"pendant une semaine. J'espère que vous comprenez notre démarche. Si vous ne respectez pas " \
               f"à nouveau les règles du blog, vous serez banni définitivement." \
               f"Pour toute information complémentaires, N'hésitez pas à répondre à ce mail afin de nous expliquez " \
               f"pourquoi vous avez été sujet au bannissement." \
               f"Cordialement. L'équipe du blog de Sethiar."
    mail.send(msg)


def definitive_banned(user):
    """
    Envoie un e-mail informant un utilisateur de son bannissement définitif du blog pour récidive dans le non-respect des règles.

    Args:
        user (User): L'utilisateur qui se fait bannir définitivement.
    """
    mail = current_app.extensions['mail']
    msg = Message("Effacement des bases de données.",
                 sender='alefetey123@gmail.com',
                 recipients=[user.email])
    msg.body = f"Bonjour {user.pseudo}," \
               f"Comme nous vous l'avions indiqué dans un précédent mail, si vous étiez de nouveau sujet à un rappel " \
               f"à l'ordre sur le respect des règles en vigueur sur notre blog, vous seriez définitivement effacé de " \
               f"nos bases de données. Le fait que vous receviez ce mail signifie que vous avez été effacé de notre " \
               f"base de données. Nous regrettons cette décision, mais nous ne pouvons tolérer ce manquement aux " \
               f"règles établies. " \
               f"Cordialement. L'équipe du blog de Sethiar."
    mail.send(msg)

