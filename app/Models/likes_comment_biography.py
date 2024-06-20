"""Classe représentant les likes pour les commentaires des utilisateurs du blog concernant les biographies."""

from . import db


# Table de liaison pour les likes des commentaires de la section biographie.
class CommentLikeBiography(db.Model):
    """
    Modèle de données représentant la relation entre les utilisateurs et les commentaires
    qu'ils aiment dans la section biographie.

    Attributes:
        user_id (int) : Identifiant de l'utilisateur qui a aimé le commentaire (clé primaire).
        comment_id (int): Identifiant du commentaire aimé (clé primaire).
    """
    __tablename__ = "likes_comment_biography"
    __table_args__ = {"extend_existing": True}

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comment_biography.id"), primary_key=True)

    def __repr__(self):
        return f"CommentLikeBiography(user_id={self.user_id}, comment_id={self.comment_id})"
