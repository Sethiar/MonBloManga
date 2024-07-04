"""Classe des articles du blog"""

from . import db
from datetime import datetime


class Article(db.Model):
    """
    Modèle de données représentant un article du blog.

    Attributes:
        id (int): Identifiant unique de l'article.
        title (str): Titre de l'article.
        author_id (int): Identifiant de l'auteur de l'article.
        resume: (str): Résumé de l'article (100 caractères max).
        article_content (str) : Contenu de l'article.
        date_edition (datetime) : Date d'édition de l'article.
        categorie_id (int) : Identifiant de la catégorie associée à l'article.
        categorie (Categorie) : Référence à l'objet Categorie associé à l'article.
        likes (int) : Nombre de likes.
        dislikes (int) : Nombre de dislikes.
    """

    __tablename__ = "article"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    resume = db.Column(db.Text(), nullable=False)
    article_content = db.Column(db.Text(), nullable=False)
    date_edition = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('articles', lazy=True))

    categorie_id = db.Column(db.Integer, db.ForeignKey("categorie.id"), nullable=False)
    categorie = db.relationship("Categorie", backref=db.backref("articles", lazy="dynamic"))

    likes = db.Column(db.Integer, nullable=False, default=0)
    dislikes = db.Column(db.Integer, nullable=False, default=0)

    # Ajout de la relation avec suppression en cascade pour les commentaires.
    comments = db.relationship('CommentArticle', backref='comment_article', cascade='all, delete-orphan')

    # Ajout des relations avec suppression en cascade pour les likes et dislikes.
    likes_rel = db.relationship('Likes', backref='liked_article', cascade='all, delete-orphan', lazy='dynamic')
    dislikes_rel = db.relationship('Dislikes', backref='disliked_article', cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet Article.

        Returns :
            str: Chaîne représentant l'objet Article.
        """
        return f"Article(Titre='{self.title}', Auteur='{self.author.pseudo}', Résumé='{self.resume}', " \
               f"Catégorie='{self.categorie}', Date d'édition='{self.date_edition}', like='{self.likes}', dislikes='{self.dislikes}')"

