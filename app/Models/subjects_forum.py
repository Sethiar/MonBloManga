"""
Classe permettant de créer l'objet "sujet" du forum.
"""

from . import db


class SubjectForum(db.Model):
    """
    Modèle de données représentant un sujet pour le forum.

    Attributes:
        id (int): Identifiant unique du sujet pour le forum.
        nom (str): Nom du sujet du forum (limité à 50 caractères).
    """

    __tablename__ = "subject_forum"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet Subject_forum.

        Returns :
            str: Chaîne représentant l'objet Subject_forum.
        """
        return f"SubjectForum(nom='{self.nom}')"
