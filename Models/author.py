"""Classe représentant les auteurs des articles."""

from Models import db


class Author(db.Model):
    """
    Modèle de données représentant un auteur d'articles.

    Attributes:
        id (int): Identifiant unique de l'auteur.
        nom (str) : Nom de l'auteur.
        prenom (str): Prénom de l'auteur.
        pseudo (str): Pseudo unique de l'auteur.
    """

    __tablename__ = "author"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(30), nullable=False)
    prenom = db.Column(db.String(30), nullable=False)
    pseudo = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet Author.

        Returns :
            str : Chaîne représentant l'objet Author.
        """
        return f"Author(Pseudo='{self.pseudo}')"
