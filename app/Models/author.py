"""Classe représentant les auteurs des articles."""

from . import db


class Author(db.Model):
    """
    Modèle de données représentant un auteur d'articles.

    Attributes:
        id (int): Identifiant unique de l'auteur.
        nom (str): Nom de famille de l'auteur.
        prenom (str): Prénom de l'auteur.
        pseudo (str): Pseudo unique de l'auteur.
    """

    __tablename__ = "author"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(30), nullable=False)
    prenom = db.Column(db.String(30), nullable=False)
    pseudo = db.Column(db.String(30), unique=True, nullable=False)
    # Relation avec la classe BiographyMangaka.
    biographies = db.relationship('BiographyMangaka', backref='author_biographies', lazy=True)

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet Author.

        Returns :
            str : Chaîne représentant l'objet Author.
        """
        return f"Author(id={self.id}, pseudo='{self.pseudo}')"
