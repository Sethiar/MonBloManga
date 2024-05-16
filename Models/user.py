"""Modèle de la classe Utilisateur."""

import logging

from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """
    Modèle de données représentant un utilisateur de l'application.

    Attributes:
        id (int): Identifiant unique de l'utilisateur.
        pseudo (str): Pseudo unique de l'utilisateur.
        password_hash (bytes): Mot de passe hashé de l'utilisateur.
        salt (bytes): Salage du mot de passe.
        email (str): Adresse e-mail de l'utilisateur.
        date_naissance (datetime.date): Date de naissance de l'utilisateur.
        banned (bool): Indique si l'utilisateur est banni (par défaut False).
    """

    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(30), nullable=False, unique=True)
    password_hash = db.Column(db.LargeBinary(255), nullable=False)
    salt = db.Column(db.LargeBinary(254), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    banned = db.Column(db.Boolean, default=False)


    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet Utilisateur.

        Returns :
            str: Chaîne représentant l'objet Utilisateur.
        """
        return f"User(pseudo='{self.pseudo}', email='{self.email}', date_naissance='{self.date_naissance}', banned='{self.banned}')"

    def is_active(self):
        """
        Indique si l'utilisateur est actif.

        Returns :
            bool : False car l'utilisateur n'est pas banni par défault.
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

