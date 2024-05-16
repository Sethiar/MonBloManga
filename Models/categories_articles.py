"""Classe représentant une catégorie d'articles."""

from . import db


class Categorie(db.Model):
    """
    Modèle de données représentant une catégorie d'articles.

    Attributes:
        id (int) : Identifiant unique de la catégorie.
        nom (str) : Nom de la catégorie.
    """

    __tablename__ = "categorie"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet Catégorie.

        Returns :
            str: Chaîne représentant l'objet Catégorie.
        """
        return f"Categorie(nom='{self.nom}')"
