"""Script qui permet de créer l'application,
il contient toute la configuration nécessaire afin que le script fonctionne."""

import logging
import os
import secrets
import config

from flask import Flask, session
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail


from datetime import timedelta

from Models.user import User
from Models.admin import Admin
from Models.anonyme import Anonyme
from Models import db

from app.auth import auth_bp
from app.admin import admin_bp
from app.user import user_bp
from app.functional import functional_bp
from app.frontend import frontend_bp
from app.mail import mail_bp

from login_manager import login_manager
from config import Config
from app.extensions import mail


def create_app():
    """
    Crée et configure l'application Flask pour le blog.

    :return: L'application Flask créée.
    """

    # Création de l'instance Flask.
    app = Flask("MonBlogManga")

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'alefetey123@gmail.com'
    app.config['MAIL_PASSWORD'] = 'zrjo ahkg vwid hfap'
    app.config['MAIL_DEFAULT_SENDER'] = 'alefetey123@gmail.com'

    mail.init_app(app)

    # Charger la configuration de l'environnement.
    if os.environ.get("FLASK_ENV") == "development":
        app.config.from_object(config.DevelopmentConfig)
    elif os.environ.get("FLASK_ENV") == "testing":
        app.config.from_object(config.TestingConfig)
    else:
        app.config.from_object(config.ProductConfig)

    # Configuration de l'environnement de l'application.
    app.config.from_object(Config)

    app.config["SESSION_COOKIE_SECURE"] = True

    # Définition de la clé secrète pour les cookies.
    app.secret_key = secrets.token_hex(16)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(functional_bp, url_prefix='/functional')
    app.register_blueprint(frontend_bp, url_prefix='/frontend')
    app.register_blueprint(mail_bp, url_prefix='/mail')

    # Propagation des erreurs aux gestionnaires d'erreurs des Blueprints.
    app.config['PROPAGATE_EXCEPTIONS'] = True

    @login_manager.user_loader
    def load_user(user_id):
        """
        Charge un utilisateur à partir de la base de données en utilisant son ID.

        :param user_id: L'identifiant de l'utilisateur.
        Returns: L'objet User ou Admin chargé depuis la base de données.
        """
        user = User.query.get(user_id)
        admin = Admin.query.get(user_id)

        if user:
            return user
        if admin:
            return admin

        return None

    @app.context_processor
    def inject_logged_in():
        """
        Injecte le statut de connexion et le pseudo de l'utilisateur dans le contexte global de l'application.
        """
        logged_in = session.get("logged_in", False)
        pseudo = session.get("pseudo", None)
        return dict(logged_in=logged_in, pseudo=pseudo)

    # Initialisation de la classe à utiliser pour les utilisateurs anonymes.
    login_manager.init_app(app)
    login_manager.anonymous_user = Anonyme

    # Configuration de la durée de vie des cookies de session (optionnel)
    app.permanent_session_lifetime = timedelta(days=1)  # Durée de vie d'un jour pour les cookies de session

    # Configuration de la journalisation.
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    app.logger.setLevel(logging.DEBUG)
    app.logger.debug("Message de débogage")
    app.logger.info("Message informatif")
    app.logger.warning("Message d'avertissement")
    app.logger.error("Message d'erreur")
    handler = logging.FileHandler("fichier.log")
    app.logger.addHandler(handler)

    # Configuration de l'application pour utiliser la protection CSRF.
    csrf = CSRFProtect(app)

    # Initialisation de la base de données.
    db.init_app(app)

    return app