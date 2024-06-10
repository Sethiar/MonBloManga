"""Classe représentant les likes et les dislikes pour les articles pour les utilisateurs du blog."""

from . import db


# Table de liaison pour les likes
class Likes(db.Model):
    """
    Modèle de données représentant la relation entre les utilisateurs et les articles qu'ils aiment.

    Attributes:
        user_id (int) : Identifiant de l'utilisateur.
        article_id (int) : Identifiant de l'article.
    """

    __tablename__ = "likes"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"), primary_key=True)

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet Likes.

        Returns :
            str: Chaîne représentant l'objet Likes.
        """
        return f"Likes(user_id='{self.user_id}', article_id='{self.article_id}')"


# Table de liaison pour les dislikes
class Dislikes(db.Model):
    """
        Modèle de données représentant la relation entre les utilisateurs et les articles qu'ils n'aiment pas.

        Attributes:
            user_id (int) : Identifiant de l'utilisateur.
            article_id (int) : Identifiant de l'article.
        """
    __tablename__ = "dislikes"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"), primary_key=True)

    def __repr__(self):
        return f"Dislikes(user_id='{self.user_id}', article_id='{self.article_id}')"

