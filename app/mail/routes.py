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
    """
    msg = Message("Hello",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=["alefetey123@gmail.com"])
    msg.body = "Ce mail est un mail test permettant de vérifier le fonctionnement du serveur SMTP."
    current_app.extensions['mail'].send(msg)
    return "Email envoyé !"


@mail_bp.route("/send_confirmation_email/<string:email>")
def send_confirmation_email(email):
    """
    Envoie un e-mail de confirmation d'inscription à un nouvel utilisateur.
    """
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Utilisateur non trouvé.", "attention")
        return redirect(url_for('landing_page'))

    msg = Message("Confirmation d'inscription", sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
    msg.body = f"Merci de vous être inscrit sur notre site. Votre inscription a été confirmée avec succès.\n" \
               f"Nous espérons que nous vous retrouverons bientôt afin d'entendre votre voix sur notre blog.\n" \
               f"Merci {user.pseudo} de votre confiance."
    current_app.extensions['mail'].send(msg)
    return redirect(url_for('landing_page'))


def mail_birthday():
    """
    Envoie des e-mails de souhaits d'anniversaire aux utilisateurs dont c'est l'anniversaire aujourd'hui.
    """
    today = date.today()
    users = User.query.filter(db.extract('month', User.date_naissance) == today.month,
                              db.extract('day', User.date_naissance) == today.day).all()
    for user in users:
        send_birthday_email(user)


def send_birthday_email(user):
    """
    Envoie un e-mail de souhaits d'anniversaire à un utilisateur spécifique.
    """
    msg = Message("Joyeux anniversaire !",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])
    msg.body = f"Bonjour {user.pseudo},\n\nNous vous souhaitons un très joyeux anniversaire !\n" \
               f"\nCordialement,\nL'équipe du blog."
    current_app.extensions['mail'].send(msg)


def mail_banned_user(user):
    """
    Envoie un e-mail informant un utilisateur de son bannissement temporaire pour non-respect des règles.
    """
    msg = Message("Bannissement",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])
    msg.body = f"Bonjour {user.pseudo},\n" \
               f"Suite à la tenue des règles en vigueur sur le blog, vous avez été banni " \
               f"pendant une semaine. J'espère que vous comprenez notre démarche. Si vous ne respectez pas " \
               f"à nouveau les règles du blog, vous serez banni définitivement.\n" \
               f"Cordialement, L'équipe du blog."
    current_app.extensions['mail'].send(msg)


def definitive_banned(user):
    """
    Envoie un e-mail informant un utilisateur de son bannissement définitif du blog pour récidive dans le non-respect des règles.
    """
    msg = Message("Effacement des bases de données.",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])
    msg.body = f"Bonjour {user.pseudo},\n" \
               f"Comme nous vous l'avions indiqué dans un précédent mail, si vous étiez de nouveau sujet à un rappel " \
               f"à l'ordre sur le respect des règles en vigueur sur notre blog, vous seriez définitivement effacé de " \
               f"nos bases de données. Le fait que vous receviez ce mail signifie que vous avez été effacé de notre " \
               f"base de données. Nous regrettons cette décision, mais nous ne pouvons tolérer ce manquement aux " \
               f"règles établies.\n" \
               f"Cordialement, L'équipe du blog."
    current_app.extensions['mail'].send(msg)

