"""Classe représentant les likes pour les réponses des commentaires des utilisateurs du blog."""

from . import db


# Table de liaison pour les likes des commentaires.
class CommentLike(db.Models):
    """
    Modèle de données représentant la relation entre les utilisateurs et les réponses aux commentaires qu'ils aiment.

    Attributes:
        user_id (int) : Identifiant de l'utilisateur.
        comment_reply_id (int) : Identifiant du commentaire.
        """
    __tablename__ = "likes_comment"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("comment.id"), primary_key=True)

    def __repr__(self):
        return f"LikesComment(user_id='{self.user_id}', comment_id='{self.comment_id}')"
