"""
Représente la classe des réponses aux commentaires des articles.
"""

from . import db
from datetime import datetime


class Reply(db.Model):
    """
    Représente une réponse à un commentaire.

    Attributes:
        id (int): Identifiant de la réponse.
        contenu (str): Contenu de la réponse au commentaire.
        date (date): Date de la réponse.
        commentaire_id (int): Identifiant du commentaire associé à la réponse.
        likes (int): Nombre de likes.
        dislikes (int): Nombre de  dislikes.
    """
    __tablename__ = "reply"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    reply_content = db.Column(db.Text(), nullable=False)
    reply_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Comptage des likes.
    reply_likes = db.Column(db.Integer, nullable=False, default=0)
    reply_dislikes = db.Column(db.Integer, nullable=False, default=0)

    # Relation avec la classe Comment.
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    comment = db.relationship('Comment', backref=db.backref('replies', lazy=True))

    # Relation avec la classe User.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('replies', lazy=True))

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet Reply.

        Returns :
            str: Chaîne représentant l'objet Reply.
        """
        return f"Reply(id={self.id}, comment_id={self.comment_id}, user_id={self.user_id}, " \
               f"date={self.reply_date}, like={self.reply_likes}, dislikes={self.reply_dislikes})"
