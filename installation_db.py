"""
Ce fichier définit les modèles de données SQLAlchemy pour l'application, y compris les tables pour enregistrer les informations des utilisateurs, des administrateurs, des articles et des catégories.

Classes de modèles de données :
    - Admin : Représente un administrateur de l'application avec un identifiant unique, un rôle, un identifiant et un mot de passe hashé.
    - User : Représente un utilisateur de l'application avec un identifiant unique, un nom, un prénom, une adresse e-mail, une date de naissance et un genre.
    - Author : Représente un auteur avec un identifiant unique, un nom, un prénom et un pseudo unique.
    - Article : Représente un article avec un identifiant unique, un titre, un nom d'auteur, un contenu et une date d'édition.
    - Categorie : Représente une catégorie avec un identifiant unique et un nom.

Les tables sont créées dans ce contexte d'application Flask pour garantir leur installation correcte.
"""
from Models import db
from flask_login import UserMixin
from app.create_app import create_app

from datetime import datetime

app = create_app()

# L'installation des tables doit se faire dans ce contexte.
with app.app_context():
    # Modèle de la classe Admin
    class Admin(db.Model, UserMixin):
        """
        Représente un administrateur de l'application.

        Attributes:
            id (int): Identifiant unique de l'administrateur.
            role (str): Rôle de l'administrateur.
            identifiant (str): Identifiant de connexion de l'administrateur.
            password_hash (str): Mot de passe hashé de l'administrateur.
            salt (str): Salage du mot de passe.
        """
        __tablename__ = "admin"
        __table_args__ = {"extend_existing": True}

        id = db.Column(db.Integer, primary_key=True)
        role = db.Column(db.String(20), nullable=False)
        identifiant = db.Column(db.String(30), nullable=False)
        password_hash = db.Column(db.LargeBinary(255), nullable=False)
        salt = db.Column(db.LargeBinary(254), nullable=False)

    # Modèle de la classe User.
    class User(db.Model, UserMixin):
        """
        Représente un utilisateur de l'application.

        Attributes:
            id (int): Identifiant unique de l'utilisateur.
            pseudo (str): Pseudo unique de l'utilisateur.
            password_hash (int): Password hashé par bcrypt.
            salt (str): Processus de salage du mot de passe.
            email (str): Adresse e-mail de l'utilisateur.
            date_naissance (date): Date de naissance de l'utilisateur.
            banned (bool): renseigne sur l'état de bannissement de l'utilisateur.
        """
        __tablename__ = "user"
        __table_args__ = {"extend_existing": True}

        id = db.Column(db.Integer, primary_key=True)
        pseudo = db.Column(db.String(30), nullable=False, unique=True)
        password_hash = db.Column(db.LargeBinary(255), nullable=False)
        salt = db.Column(db.LargeBinary(254), nullable=False)
        email = db.Column(db.String(255), nullable=False)
        date_naissance = db.Column(db.Date, nullable=False)
        banned = db.Column(db.Boolean, default=False)

    # Modèle de la classe Author.
    class Author(db.Model):
        """
        Représente un auteur.

        Attributes:
            id (int): Identifiant unique de l'auteur.
            nom (str): Nom de l'auteur.
            prenom (str): Prénom de l'auteur.
            pseudo (str): Pseudo unique de l'auteur.
        """
        __tablename__ = "author"
        __table_args__ = {"extend_existing": True}

        id = db.Column(db.Integer, primary_key=True)
        nom = db.Column(db.String(30), nullable=False)
        prenom = db.Column(db.String(30), nullable=False)
        pseudo = db.Column(db.String(30), unique=True, nullable=False)

    # Modèle de la classe Article.
    class Article(db.Model):
        """
        Représente un article.

        Attributes:
            id (int): Identifiant unique de l'article.
            title (str): Titre de l'article.
            resume (str): Résumé de l'article.
            article_content (str): Contenu de l'article.
            date_edition (date): Date d'édition de l'article.
            pseudo_author (str): Pseudo de l'auteur de l'article.
            author (Author): Relation avec la classe Author.
            categorie_id (int): Identifiant de la catégorie de l'article.
            categorie (Categorie): Relation avec la classe Categorie.
            likes (int): Nombre de likes.
            dislikes (int): Nombre de dislikes.
        """
        __tablename__ = "article"
        __table_args__ = {"extend_existing": True}

        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(50), unique=True, nullable=False)
        resume = db.Column(db.Text(), nullable=False)
        article_content = db.Column(db.Text(), nullable=False)
        date_edition = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        # Comptage des likes et dislikes.
        likes = db.Column(db.Integer, nullable=False, default=0)
        dislikes = db.Column(db.Integer, nullable=False, default=0)

        # Pseudo de l'auteur de l'article.
        pseudo_author = db.Column(db.String(30), db.ForeignKey('author.pseudo'), nullable=True)

        # Relation avec la classe Author.
        author = db.relationship('Author', backref=db.backref('articles', lazy=True))

        # Relation avec la classe catégorie.
        categorie_id = db.Column(db.Integer, db.ForeignKey("categorie.id"), nullable=False)
        categorie = db.relationship("Categorie", backref=db.backref("articles", lazy="dynamic"))

    # Modèle de la classe Catégorie.
    class Categorie(db.Model):
        """
        Représente une catégorie.

        Attributes:
            id (int): Identifiant unique de la catégorie.
            nom (str): Nom de la catégorie.
        """
        __tablename__ = "categorie"
        __table_args__ = {"extend_existing": True}

        id = db.Column(db.Integer, primary_key=True)
        nom = db.Column(db.String(50), nullable=False)

    # Modèle de la classe sujet pour le forum.
    class SubjectForum(db.Model):
        """
        Représente un sujet.

        Attributes:
            id (int): Identifiant unique du sujet du forum.
            nom (str): Nom du sujet.
        """
        __tablename__ = "subject_forum"
        __table_args__ = {"extend_existing": True}

        id = db.Column(db.Integer, primary_key=True)
        nom = db.Column(db.String(50), nullable=False)

    # Modèle de la classe Comment pour les articles.
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
        article = db.relationship('Article', backref=db.backref('comments', lazy=True))

        # Relation avec la classe User.
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        user = db.relationship('User', backref=db.backref('article_comments', lazy=True))

    # Modèle de la classe Comment pour les sujets du forum.
    class CommentSubject(db.Model):
        """
        Représente un commentaire pour un sujet du forum.

        Attributes:
            id (int): Identifiant unique du commentaire.
            comment_content (str): Contenu du commentaire.
            comment_date (date): Date du commentaire.
            subject_id (int): Identifiant de l'article associé au commentaire.
            user_id (int): Identifiant de l'utilisateur enregistré.
        """
        __tablename__ = "comment_subject"
        __table_args__ = {"extend_existing": True}

        id = db.Column(db.Integer, primary_key=True)
        comment_content = db.Column(db.Text(), nullable=False)
        comment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        # Relation avec la classe SubjectForum.
        subject_id = db.Column(db.Integer, db.ForeignKey('subject_forum.id'), nullable=False)
        subject = db.relationship('SubjectForum', backref=db.backref('comments', lazy=True))

        # Relation avec la classe User.
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        user = db.relationship('User', backref=db.backref('subject_comments', lazy=True))

    class Likes(db.Model):
        """
        Modèle de données représentant la relation entre les utilisateurs et les articles qu'ils aiment.

        Attributes:
            user_id (int) : Identifiant de l'utilisateur.
            article_id (int) : Identifiant de l'article.
        """
        __tablename__ = "likes"
        __table_args__ = {"extend_existing": True}

        user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
        article_id = db.Column(db.Integer, db.ForeignKey("article.id"), primary_key=True)

    # Table de liaison pour les dislikes
    class Dislikes(db.Model):
        """
        Modèle de données représentant la relation entre les utilisateurs et les articles qu'ils n'aiment pas.

        Attributes:
            user_id (int) : Identifiant de l'utilisateur.
            article_id (int) : Identifiant de l'article.
        """
        __tablename__ = "dislikes"
        __table_args__ = {"extend_existing": True}

        user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
        article_id = db.Column(db.Integer, db.ForeignKey("article.id"), primary_key=True)

    class CommentLikeArticle(db.Model):
        """
        Modèle de données représentant la relation entre les utilisateurs et les commentaires
        qu'ils aiment de la section article.

        Attributes:
            user_id (int) : Identifiant de l'utilisateur.
            comment_id (int) : Identifiant du commentaire.
            """
        __tablename__ = "likes_comment_article"
        __table_args__ = {"extend_existing": True}

        user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
        comment_id = db.Column(db.Integer, db.ForeignKey("comment_article.id"), primary_key=True)

    class CommentLikeSubject(db.Model):
        """
        Modèle de données représentant la relation entre les utilisateurs et les commentaires
        qu'ils aiment de la section forum.

        Attributes:
            user_id (int) : Identifiant de l'utilisateur.
            comment_id (int) : Identifiant du commentaire.
            likes_subject_count(int) : Nombre de likes du commentaire pour le sujet.
        """
        __tablename__ = "likes_comment_subject"
        __table_args__ = {"extend_existing": True}

        user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
        comment_id = db.Column(db.Integer, db.ForeignKey("comment_subject.id"), primary_key=True)

    class ReplyArticle(db.Model):
        """
        Représente une réponse à un commentaire sur un article.

        Attributes:
            id (int): Identifiant unique de la réponse.
            reply_content (str): Contenu de la réponse.
            reply_date (date): Date de la réponse.
            comment_id (int): Identifiant du commentaire associé à la réponse.
            user_id (int): Identifiant de l'utilisateur ayant posté la réponse.
        """
        __tablename__ = "reply_article"
        __table_args__ = {"extend_existing": True}

        id = db.Column(db.Integer, primary_key=True)
        reply_content = db.Column(db.Text(), nullable=False)
        reply_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        # Relation avec la classe CommentArticle.
        comment_id = db.Column(db.Integer, db.ForeignKey('comment_article.id'), nullable=False)
        comment = db.relationship('CommentArticle', backref=db.backref('replies', lazy=True))

        # Relation avec la classe User.
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        user = db.relationship('User', backref=db.backref('article_replies', lazy=True))


    class ReplySubject(db.Model):
        """
        Représente une réponse à un commentaire sur un sujet du forum.

        Attributes:
            id (int): Identifiant unique de la réponse.
            reply_content (str): Contenu de la réponse.
            reply_date (date): Date de la réponse.
            comment_id (int): Identifiant du commentaire associé à la réponse.
            user_id (int): Identifiant de l'utilisateur ayant posté la réponse.
        """
        __tablename__ = "reply_subject"
        __table_args__ = {"extend_existing": True}

        id = db.Column(db.Integer, primary_key=True)
        reply_content = db.Column(db.Text(), nullable=False)
        reply_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        # Relation avec la classe CommentSubject.
        comment_id = db.Column(db.Integer, db.ForeignKey('comment_subject.id'), nullable=False)
        comment = db.relationship('CommentSubject', backref=db.backref('replies', lazy=True))

        # Relation avec la classe User.
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        user = db.relationship('User', backref=db.backref('subject_replies', lazy=True))

    # Création de toutes les tables à partir de leur classe.
    db.create_all()

print("Félicitations, toutes vos tables ont été installées.")
