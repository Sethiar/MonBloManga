"""Classe représentant les likes pour les réponses des commentaires des utilisateurs du blog."""

from . import db


# Table de liaison pour les likes des commentaires de la section forum.
class CommentLikeSubject(db.Model):
    """
    Modèle de données représentant la relation entre les utilisateurs et les commentaires
    qu'ils aiment de la section forum.

    Attributes:
        user_id (int) : Identifiant de l'utilisateur.
        comment_id (int) : Identifiant du commentaire.
    """
    __tablename__ = "likes_comment_subject"
    __table_args__ = {"extend_existing": True}

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comment_subject.id"), primary_key=True)
    likes_subject_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"CommentLikeSubject(user_id={self.user_id}, comment_id={self.comment_id}," \
               f"likes_subject_count={self.likes_subject_count})"
