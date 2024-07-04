"""
Code permettant de définir les routes concernant le mailing du blog.
"""

from app.mail import mail_bp
from flask import redirect, url_for, flash, current_app

from flask_mail import Message

from app.Models.user import User
from app.email_utils import send_email_in_background


# Méthode qui permet d'envoyer un mail de test.
@mail_bp.route("/send_mail")
def send_email_test():
    """
    Envoie un e-mail de test à une adresse prédéfinie pour vérifier la configuration de Flask-Mail.
    """
    msg = Message("Hello",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=["alefetey123@gmail.com"])
    msg.body = "Ce mail est un mail test permettant de vérifier le fonctionnement du serveur SMTP."
    current_app.extensions['mail'].send(msg)
    return "Email envoyé !"


# Méthode qui envoie un mail de confirmation d'inscription."
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
               f"Merci {user.pseudo} de votre confiance. \n" \
               f"Mangament, \n" \
               f"L'équipe du blog."

    current_app.extensions['mail'].send(msg)
    return redirect(url_for('landing_page'))


# Méthode qui permet d'envoyer un mail à tous les utilisateurs lors de la publication d'un nouvel article.
def mail_edit_article(email, article):
    """
    Envoie des emails à tous les utilisateurs lors de la publication d'un nouvel article.
    :return:
    """
    msg = Message("Publication d'un nouvel article",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
    msg.body = f"Un nouvel article a été publié : {article.title}." \
               f"Venez donner votre avis sur le blog.\n" \
               f"Mangament,\n" \
               f"L'équipe du blog."

    try:
        current_app.extensions['mail'].send(msg)
    except Exception as e:
        current_app.logger.error(f"Erreur lors de l'envoi du mail à {email} :{str(e)}")


# Méthode qui renvoie le mail de bon anniversaire à l'utilisateur.
def send_birthday_email(email):
    """
    Envoie un e-mail de souhaits d'anniversaire à un utilisateur spécifique.
    """
    user = User.query.filter_by(email=email).first()
    msg = Message("Joyeux anniversaire !",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email])
    msg.body = f"Bonjour {user.pseudo},\n\nNous vous souhaitons un très joyeux anniversaire !\n" \
               f"\nMangament,\n" \
               f"L'équipe du blog."
    current_app.extensions['mail'].send(msg)


# Méthode qui avertit l'utilisateur de son bannissement pendant 7 jours.
def mail_banned_user(email):
    """
    Envoie un e-mail informant un utilisateur de son bannissement temporaire pour non-respect des règles.
    :param email: email de l'utilisateur qui subit le bannissement.
    :return : retour sur la page admin.
    """
    user = User.query.filter_by(email=email).first()

    msg = Message("Bannissement",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email])
    msg.body = f"Bonjour {user.pseudo},\n" \
               f"Suite à la tenue des règles en vigueur sur le blog, vous avez été banni " \
               f"pendant une semaine. J'espère que vous comprenez notre démarche. Si vous ne respectez pas " \
               f"à nouveau les règles du blog, vous serez banni définitivement.\n" \
               f"Cordialement,\n" \
               f"L'équipe du blog."
    current_app.extensions['mail'].send(msg)


# Méthode qui envoie un mail prévenant de la fin du bannissement.
def mail_deban_user(email):
    """
    Envoie un e-mail informant un utilisateur de la fin de son bannissement.
    :param email: email de l'utilisateur qui subit le bannissement.
    :return: retour sur la page admin.
    """
    user = User.query.filter_by(email=email).first()
    msg = Message("Fin de bannissement",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email])
    msg.body = f"Bonjour {user.pseudo}, \n" \
               f"Nous vous informons que vous n'êtes plus banni du blog. \n" \
               f"Nous espérons vous revoir très vite. \n" \
               f"À bientôt.\n"\
               f"Cordialement, \n" \
               f"L'équipe du blog."

    current_app.extensions['mail'].send(msg)


# Méthode qui permet d'avertir l'utilisateur de son bannissement définitif du blog.
def definitive_banned(email):
    """
    Envoie un e-mail informant un utilisateur de son bannissement définitif du blog pour récidive dans le non-respect des règles.
    :param email: email de l'utilisateur qui subit le bannissement.
    """
    user = User.query.filter_by(email=email).first()
    msg = Message("Effacement des bases de données.",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email])
    msg.body = f"Bonjour {user.pseudo},\n" \
               f"Comme nous vous l'avions indiqué dans un précédent mail, si vous étiez de nouveau sujet à un rappel " \
               f"à l'ordre sur le respect des règles en vigueur sur notre blog, vous seriez définitivement effacé de " \
               f"nos bases de données. Le fait que vous receviez ce mail signifie que vous avez été effacé de notre " \
               f"base de données. Nous regrettons cette décision, mais nous ne pouvons tolérer ce manquement aux " \
               f"règles établies.\n" \
               f"Cordialement,\n" \
               f"L'équipe du blog."
    current_app.extensions['mail'].send(msg)


# Méthode qui envoie le lien permettant de faire le changement du mot de passe.
def reset_password_mail(email, reset_url):
    """
    Envoie un mail afin de cliquer sur un lien permettant la réinitialisation du mot de passe.
    Si l'utilisateur n'est pas à l'origine de cette action, le mail inclut un lien d'alerte pour l'administrateur.

    :param reset_url: URL pour réinitialiser le mot de passe
    :param email: Adresse email du destinataire
    :return: None
    """
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Utilisateur non trouvé.", "attention")
        return redirect(url_for('landing_page'))
    msg = Message('Réinitialisation de votre mot de passe',
                  sender='noreply@yourapp.com',
                  recipients=[email])
    msg.body = f'Bonjour {user.pseudo},\n' \
               f' pour réinitialiser votre mot de passe, cliquez sur le lien suivant : {reset_url}'
    current_app.extensions['mail'].send(msg)


# Méthode qui envoie un mail assurant le succès de la réinitialisation du mail.
def password_reset_success_email(user):
    """
    Envoie un e-mail de confirmation de réinitialisation de mot de passe à l'utilisateur.

    :param user: Instance de l'utilisateur.
    """
    msg = Message('Confirmation de réinitialisation de mot de passe',
                  sender='noreply@yourapp.com',
                  recipients=[user.email])
    msg.body = f"Bonjour {user.pseudo},\n" \
               f"Votre mot de passe a été réinitialisé avec succès.\n" \
               f"Mangament,\n" \
               f"Votre équipe de support."
    current_app.extensions['mail'].send(msg)


# Méthode qui permet d'envoyer un mail à un utilisateur si quelqu'un a
# répondu à son commentaire dans la section article.
def mail_reply_comment_article(email, article_title):
    """
    Envoie un mail à l'auteur du commentaire en cas de réponse à celui-ci.
    :param email : email de l'utilisateur qui a commenté l'article.
    :param article_id : id de l'article qui a été commenté.
    :param article_title : titre de l'article qui a été commenté.
    """
    user = User.query.filter_by(email=email).first()

    msg = Message("Quelqu'un a répondu à votre commentaire de la section article.",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])
    msg.body = f"Bonjour {user.pseudo},\n" \
               f"Un utilisateur a répondu à votre commentaire de la section article " \
               f"à l'article suivant : '{article_title}'\n" \
               f"Veuillez cliquer sur ce lien pour découvrir la réponse.\n" \
               f"Mangament,\n" \
               f"Votre équipe de support."
    current_app.extensions['mail'].send(msg)


# Méthode qui permet d'envoyer un mail à un utilisateur si quelqu'un a
# répondu à son commentaire dans la section forum.
def mail_reply_forum_comment(email, subject_nom):
    """
    Envoie un mail à l'auteur du commentaire en cas de réponse à celui-ci.
    :param email: email de l'utilisateur qui a commenté le sujet du forum.
    :param subject_nom : nom du sujet du forum commenté.
    """
    user = User.query.filter_by(email=email).first()

    msg = Message("Quelqu'un a répondu à votre commentaire de la section forum.",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])
    msg.body = f"Bonjour {user.pseudo},\n" \
               f"Un utilisateur a répondu à votre commentaire de la section forum dont le sujet est {subject_nom}.\n" \
               f"Mangament,\n" \
               f"Votre équipe de support."
    current_app.extensions['mail'].send(msg)


# Méthode qui permet d'envoyer un mail à un utilisateur si quelqu'un a
# répondu à son commentaire dans la section biographie.
def mail_reply_comment_biography(email, biography_mangaka_name):
    """
    Envoie un mail à l'auteur du commentaire en cas de réponse à celui-ci.
    :param email: email de l'utilisateur qui a commenté la biographie.
    :param biography_mangaka_name : biographie à laquelle l'utilisateur a répondu.
    """

    user = User.query.filter_by(email=email).first()

    msg = Message("Quelqu'un a répondu à votre commentaire de la section biographie.",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])
    msg.body = f"Bonjour {user.pseudo},\n" \
               f"Un utilisateur a répondu à votre commentaire de la biographie de {biography_mangaka_name}.\n" \
               f"Mangament,\n" \
               f"Votre équipe de support."
    current_app.extensions['mail'].send(msg)


# Méthode qui envoie un mail à utilisateur en cas de like de son commentaire à la section article.
def mail_like_comment_article(user, article_title):
    """
    Envoie un mail à l'auteur du commentaire de la section article afin de l'avertir
    qu'un utilisateur a aimé son commentaire.
    :param user: utilisateur qui a posté le commentaire.
    :param article_title : titre de l'article qui a été commenté.
    """
    msg = Message("Quelqu'un a aimé votre commentaire de la section article.",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])
    msg.body = f"Bonjour {user.pseudo},\n" \
               f"Un utilisateur a aimé votre commentaire de la section article " \
               f"concernant l'article : {article_title}.\n" \
               f"Mangament,\n" \
               f"Votre équipe de support."
    send_email_in_background(current_app._get_current_object(), msg)


# Méthode qui envoie un mail à utilisateur en cas de like de son commentaire à la section forum.
def mail_like_comment_subject(user, subject):
    """
    Envoie un mail à l'auteur du commentaire de la section forum afin de l'avertir
    qu'un utilisateur a aimé son commentaire.
    :param user: utilisateur qui a posté le commentaire.
    :param subject: sujet dont le commentaire a été liké.
    """
    msg = Message("Quelqu'un a aimé votre commentaire de la section forum.",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])
    msg.body = f"Bonjour {user.pseudo},\n" \
               f"Un utilisateur a aimé votre commentaire de la section forum " \
               f"concernant le sujet suivant : {subject.nom}.\n" \
               f"Mangament,\n" \
               f"Votre équipe de support."
    send_email_in_background(current_app._get_current_object(), msg)


# Méthode qui envoie un mail à utilisateur en cas de like de son commentaire à la section forum.
def mail_like_comment_biography(user, biography):
    """
    Envoie un mail à l'auteur du commentaire de la section biographie afin de l'avertir
    qu'un utilisateur a aimé son commentaire.
    :param user: utilisateur qui a posté le commentaire.
    :param biography : biography dont le commentaire a été liké.
    """
    msg = Message("Quelqu'un a aimé votre commentaire de la section biographie.",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])
    msg.body = f"Bonjour {user.pseudo},\n" \
               f"Un utilisateur a aimé votre commentaire de la section biographie " \
               f"concernant la biographie de : {biography.mangaka_name}\n" \
               f"Mangament, \n" \
               f"Votre équipe de support."
    send_email_in_background(current_app._get_current_object(), msg)


