"""
Représente la classe des réponses aux commentaires des articles.
"""

from . import db
from datetime import datetime


# Table des réponses aux commentaires des articles.
class ReplyArticle(db.Model):
    """
    Représente une réponse à un commentaire sur un article.

    Attributes:
        id (int): Identifiant unique de la réponse.
        reply_content (str) : Contenu de la réponse.
        reply_date (datetime) : Date et heure de la réponse (par défaut, date actuelle UTC).
        comment_id (int) : Identifiant du commentaire associé à la réponse.
        user_id (int) : Identifiant de l'utilisateur ayant posté la réponse.
    """
    __tablename__ = "reply_article"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    reply_content = db.Column(db.Text(), nullable=False)
    reply_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relation avec la classe CommentArticle.
    comment_id = db.Column(db.Integer, db.ForeignKey('comment_article.id'), nullable=False)
    comment = db.relationship('CommentArticle', backref=db.backref('replies_comment_article', lazy=True))

    # Relation avec la classe User.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('user_comment_article_replies', lazy=True))

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet Reply.

        Returns :
            str : Chaîne représentant l'objet Reply.
        """
        return f"ReplyArticle(id={self.id}, comment_id={self.comment_id}, user_id={self.user_id}, " \
               f"date={self.reply_date}, like={self.reply_likes}, dislikes={self.reply_dislikes})"
