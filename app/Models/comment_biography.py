"""
Code de la table de données des commentaires pour les biographies.
"""

from . import db
from datetime import datetime


# Modèle de la classe Comment de la section biographie.
class CommentBiography(db.Model):
    """
    Représente un commentaire sur une biographie.

    Attributes:
        id (int) :  identifiant unique du commentaire.
        comment_content (str): Contenu du commentaire.
        comment_biography_date (str): Date du commentaire.
        biography_mangaka_id (int): Identifiant de la biographie associé au commentaire.
        user_id (int): Identifiant de l'utilisateur enregistré pour le commentaire.
    """
    __tablename__ = "comment_biography"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.Text(), nullable=False)

    # Date du commentaire.
    comment_biography_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relation avec la classe BiographyMangaka.
    biography_mangaka_id = db.Column(db.Integer, db.ForeignKey('biography_mangaka.id'), nullable=False)
    biography_mangaka = db.relationship('BiographyMangaka', backref=db.backref('comment_biography', lazy=True))

    # Relation avec la classe User.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('user_biography_comments', lazy=True))

    # Relation avec la classe ReplyBiography avec suppression en cascade.
    replies_suppress_biography = db.relationship('ReplyBiography', backref='parent_comment',
                                                 cascade='all, delete-orphan')

    # Relation avec la classe LikeCommentBiography avec suppression en cascade.
    likes_suppress_biography = db.relationship('CommentLikeBiography', backref='comment_like_biography',
                                               cascade='all, delete-orphan')

    def __repr__(self):
        """
        Rep^résentaiotn de l'objet BiographyComment.

        Returns:
            str: Chaîne représentant l'objet BiographyComment.
        """
        return f"BiographyComment(id={self.id}, biography_mangaka_id={self.biography_mangaka_id}," \
               f" user_id={self.user_id}, date={self.comment_biography_date})"

