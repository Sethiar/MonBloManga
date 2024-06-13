"""
Représente la classe des réponses aux commentaires des biographies.
"""

from . import db
from datetime import datetime


class ReplyBiography(db.Model):
    """
    Représente une réponse à un commentaire sur une biographie.

    Attributes:
        id (int): Identifiant unique de la réponse.
        reply_content (str): Contenu de la réponse.
        reply_date (date): Date de la réponse.
        comment_id (int): Identifiant du commentaire associé à la réponse.
        user_id (int): Identifiant de l'utilisateur ayant posté la réponse.
    """
    __tablename__ = "reply_biography"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    reply_content = db.Column(db.Text(), nullable=False)
    reply_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relation avec la classe CommentArticle.
    comment_id = db.Column(db.Integer, db.ForeignKey('comment_biography.id'), nullable=False)
    comment = db.relationship('CommentBiography', backref=db.backref('replies_comment_biography', lazy=True))

    # Relation avec la classe User.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('user_comment_biography_replies', lazy=True))

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet ReplyBiography.

        Returns :
            str: Chaîne représentant l'objet ReplyBiography.
        """
        return f"ReplyBiography(id={self.id}, comment_id={self.comment_id}, user_id={self.user_id}, " \
               f"date={self.reply_date}, like={self.reply_likes}, dislikes={self.reply_dislikes})"
