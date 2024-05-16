"""Script qui permet de créer l'application,
il contient toute la configuration nécessaire afin que le script fonctionne."""

import logging
import os
import secrets
import config
import uuid


from flask import Flask, session
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta

from Models.user import User
from Models.admin import Admin
from Models.anonyme import Anonyme
from Models import db


def generate_unique_id():
    """Génère un identifiant unique pour les utilisateurs anonymes.
    Returns:
        str: L'identifiant unique est généré.
        """
    return str(uuid.uuid4())


def create_app():
    """
    Crée et configure l'application Flask pour le blog.

    :return: L'application Flask créée.
    """
    # Création de l'instance Flask.
    app = Flask("MonBlogManga")

    # Charger la configuration de l'environnement.
    if os.environ.get("FLASK_ENV") == "development":
        app.config.from_object(config.DevelopmentConfig)
    elif os.environ.get("FLASK_ENV") == "testing":
        app.config.from_object(config.TestingConfig)
    else:
        app.config.from_object(config.ProductConfig)

    # Configuration de l'environnement de l'application.
    app.config.from_envvar("FLASK_APP_SETTINGS")
    app.config["SESSION_COOKIE_SECURE"] = True

    # Définition de la clé secrète pour les cookies.
    app.secret_key = secrets.token_hex(16)

    # Initialisation du gestionnaire de connexion en créant une instance LoginManager.
    login_manager = LoginManager()

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
    with app.app_context():
        db.init_app(app)

    return app, login_manager, db

