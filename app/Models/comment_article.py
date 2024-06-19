"""
Représente la classe des réponses aux commentaires des articles du blog.
"""

from . import db
from datetime import datetime


# Modèle de la classe Comment.
class CommentArticle(db.Model):
    """
    Représente un commentaire sur un article.

    Attributes:
        id (int): Identifiant unique du commentaire.
        comment_content (str): Contenu du commentaire.
        comment_date (date): Date du commentaire.
        article_id (int): Identifiant de l'article associé au commentaire.
        user_id (int): Identifiant de l'utilisateur enregistré.
    """
    __tablename__ = "comment_article"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.Text(), nullable=False)
    comment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relation avec la classe Article.
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    article = db.relationship('Article', backref=db.backref('comment_article', lazy=True))

    # Relation avec la classe User.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('user_article_comments', lazy=True))

    # Relation avec la classe ReplyArticle avec suppression en cascade.
    replies_suppress_article = db.relationship('ReplyArticle', backref='parent_comment', cascade='all, delete-orphan')

    # Relation avec la classe LikeCommentArticle avec suppression en cascade.
    likes_suppress_article = db.relationship('CommentLikeArticle', backref='comment_like_article',
                                             cascade='all, delete-orphan')

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet Comment.

        Returns :
            str: Chaîne représentant l'objet Comment.
        """
        return f"CommentArticle(id={self.id}, article_id={self.article_id}, user_id={self.user_id}, " \
               f"date={self.comment_date})"

