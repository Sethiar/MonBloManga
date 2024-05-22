
from . import db
from datetime import datetime


# Modèle de la classe Comment.
class Comment(db.Model):
    """
    Représente un commentaire sur un article.

    Attributes:
        id (int): Identifiant unique du commentaire.
        contenu (str): Contenu du commentaire.
        date (date): Date du commentaire.
        article_id (int): Identifiant de l'article associé au commentaire.
        likes (int) : Nombre de likes.
        dislikes (int) : Nombre de dislikes.
    """
    __tablename__ = "comment"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.Text(), nullable=False)
    comment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Comptage des likes et dislikes.
    likes = db.Column(db.Integer, nullable=False, default=0)
    dislikes = db.Column(db.Integer, nullable=False, default=0)

    # Relation avec la classe Article.
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    article = db.relationship('Article', backref=db.backref('comments', lazy=True))

    # Relation avec la classe User.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet Comment.

        Returns :
            str: Chaîne représentant l'objet Comment.
        """
        return f"Comment(id={self.id}, article_id={self.article_id}, user_id={self.user_id}, " \
               f"date={self.comment_date}, like={self.likes}, dislikes={self.dislikes})"
