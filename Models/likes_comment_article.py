"""Classe représentant les likes pour les commentaires des utilisateurs du blog."""

from . import db


# Table de liaison pour les likes des commentaires de la section article.
class CommentLikeArticle(db.Model):
    """
    Modèle de données représentant la relation entre les utilisateurs et les commentaires
    qu'ils aiment de la section article.

    Attributes:
        user_id (int) : Identifiant de l'utilisateur.
        comment_id (int) : Identifiant du commentaire.
    """
    __tablename__ = "likes_comment_article"
    __table_args__ = {"extend_existing": True}

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comment_article.id"), primary_key=True)

    def __repr__(self):
        return f"CommentLikeArticle(user_id={self.user_id}, comment_id={self.comment_id})"
