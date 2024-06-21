"""Modèle de la classe Utilisateur."""

from datetime import datetime, timedelta

from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """
    Modèle de données représentant un utilisateur de l'application.

    Attributes:
        id (int) : Identifiant unique de l'utilisateur.
        pseudo (str) : Pseudo unique de l'utilisateur.
        password_hash (bytes) : Mot de passe hashé de l'utilisateur.
        salt (bytes) : Salage du mot de passe.
        email (str) : Adresse e-mail de l'utilisateur.
        date_naissance (datetime.date) : Date de naissance de l'utilisateur.
        profil_photo (bytes) : Photo de profil de l'utilisateur en format binaire.
        banned (bool) : Indique si l'utilisateur est banni (par défaut False).
        date_banned : Indique la date de début du bannissement.
        date_ban_end : Permet de définir la date de fin du bannissement.
    """

    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(30), nullable=False, unique=True)
    password_hash = db.Column(db.LargeBinary(255), nullable=False)
    salt = db.Column(db.LargeBinary(254), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    profil_photo = db.Column(db.LargeBinary, nullable=False)
    banned = db.Column(db.Boolean, default=False)
    date_banned = db.Column(db.DateTime, nullable=True)
    date_ban_end = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet Utilisateur.

        Returns :
            str: Chaîne représentant l'objet Utilisateur.
        """
        return f"User(pseudo='{self.pseudo}', email='{self.email}', date_naissance='{self.date_naissance}', " \
               f"chemin_photo='{self.chemin_photo}, banned='{self.banned}', date_banned='{self.date_banned}'" \
               f"date_ban_end='{self.date_ban_end}')"

    def is_active(self):
        """
        Indique si l'utilisateur est actif.

        Returns :
            bool: True si l'utilisateur n'est pas banni, False sinon.
        """
        return not self.banned

    def is_anonymous(self):
        """
        Indique si l'utilisateur est anonyme.

        Returns :
            bool : False car l'utilisateur n'est jamais anonyme.
        """
        return False

    def get_id(self):
        """
        Récupère l'identifiant de l'utilisateur.

        Returns :
            str : L'identifiant de l'utilisateur.
        """
        return str(self.id)

    def ban_user(self):
        """
        Bannit l'utilisateur en définissant banned à True.
        """
        self.banned = True
        self.date_banned = datetime.now()
        self.date_ban_end = datetime.now() + timedelta(days=7)
        db.session.commit()

    def unban_user(self):
        """
        Débannit l'utilisateur en définissant banned à False.
        """
        self.banned = False
        self.date_banned = None
        self.date_ban_end = None
        db.session.commit()

    def is_banned(self):
        """
        Vérifie si l'utilisateur est actuellement banni.
        """
        if self.banned and self.date_ban_end:
            return datetime.now() < self.date_ban_end
        return False

