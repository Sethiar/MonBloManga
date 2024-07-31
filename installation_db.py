"""
Ce fichier définit les modèles de données SQLAlchemy pour l'application, y compris les tables pour enregistrer
les informations des utilisateurs, des administrateurs, des articles et des catégories.

Classes de modèles de données :
    - Admin : Représente un administrateur de l'application avec un identifiant unique, un rôle,
    un identifiant et un mot de passe hashé.
    - User : Représente un utilisateur de l'application avec un identifiant unique, un nom, un prénom,
    une adresse e-mail, une date de naissance et un genre.
    - Author : Représente un auteur avec un identifiant unique, un nom, un prénom et un pseudo unique.
    - Article : Représente un article avec un identifiant unique, un titre, un nom d'auteur, un contenu et une date d'édition.
    - Categorie : Représente une catégorie avec un identifiant unique et un nom.

Les tables sont créées dans ce contexte d'application Flask pour garantir leur installation correcte.
"""
from app.Models import db
from flask_login import UserMixin
from app import create_app

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
            nom (str): Nom de l'administrateur.
            prenom (str): Prénom de l'administrateur.
            pseudo (str): Pseudo de l'administrateur.
            role (str): Rôle de l'administrateur.
            password_hash (str): Mot de passe hashé de l'administrateur.
            salt (str): Salage du mot de passe.
        """
        __tablename__ = "admin"
        __table_args__ = {"extend_existing": True}

        id = db.Column(db.Integer, primary_key=True)
        pseudo = db.Column(db.String(30), nullable=False)
        role = db.Column(db.String(20), nullable=False)
        email = db.Column(db.String(255), nullable=True)
        profil_photo = db.Column(db.LargeBinary, nullable=True)
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
            profil_photo (string): url de récupération des photos utilisateurs du blog.
            banned (bool): renseigne sur l'état de bannissement de l'utilisateur.
            count_ban : Visualise le nombre de ban de l'utilisateur.
        """
        __tablename__ = "user"
        __table_args__ = {"extend_existing": True}

        id = db.Column(db.Integer, primary_key=True)
        pseudo = db.Column(db.String(30), nullable=False, unique=True)
        password_hash = db.Column(db.LargeBinary(255), nullable=False)
        salt = db.Column(db.LargeBinary(254), nullable=False)
        email = db.Column(db.String(255), nullable=False)
        date_naissance = db.Column(db.Date, nullable=False)
        profil_photo = db.Column(db.LargeBinary, nullable=False)
        role = db.Column(db.String(30), default='Utilisateur')
        banned = db.Column(db.Boolean, default=False)
        date_banned = db.Column(db.DateTime, nullable=True)
        date_ban_end = db.Column(db.DateTime, nullable=True)
        count_ban = db.Column(db.Integer, default=0)

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
        # Relation avec la classe BiographyMangaka.
        biographies = db.relationship('BiographyMangaka', backref='author_biographies', lazy=True)

    # Modèle de la classe Article.
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
        dislikes_rel = db.relationship('Dislikes', backref='disliked_article', cascade='all, delete-orphan',
                                       lazy='dynamic')

    # Table de données concernant les biographies des mangakas.
    class BiographyMangaka(db.Model):
        """
        Modèle de données représentant les biographies des mangakas.

        Attributes:
            id (int): Identifiant unique de la biographie.
            biography_content (str) : Contenu de la biographie du mangaka.
            date_bio_mangaka (datetime) : Date d'édition de la biographie.
            mangaka_name (str) : Nom du mangaka concerné par la biographie.
            author_id (int) : Identifiant de l'auteur de la biographie.
            author (Author): Référence à l'objet Author associé à l'auteur de la biographie.
            likes (int): Nombre de likes pour la biographie.
            dislikes (int): Nombre de dislikes pour la biographie.
        """
        __tablename__ = "biography_mangaka"
        __table_args__ = {"extend_existing": True}

        id = db.Column(db.Integer, primary_key=True)
        biography_content = db.Column(db.Text(), nullable=False)

        # Date d'édition de la biographie.
        date_bio_mangaka = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        # Nom du mangaka.
        mangaka_name = db.Column(db.String(50), nullable=False)

        # Relation avec la classe Author.
        author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
        author = db.relationship('Author', backref=db.backref('biography_mangaka_author', lazy=True))

        likes = db.Column(db.Integer, nullable=False, default=0)
        dislikes = db.Column(db.Integer, nullable=False, default=0)

        # Ajout de la relation avec suppression en cascade pour les commentaires.
        comments = db.relationship('CommentBiography', backref='comment_biography', cascade='all, delete-orphan')

        # Ajout des relations avec suppression en cascade pour les likes et dislikes.
        likes_rel = db.relationship('LikesBiography', backref='liked_biography',
                                    cascade='all, delete-orphan', lazy='dynamic')
        dislikes_rel = db.relationship('DislikesBiography', backref='disliked_biography',
                                       cascade='all, delete-orphan', lazy='dynamic')

    # Modèle de la classe Catégorie.
    class Categorie(db.Model):
        """
        Représente une catégorie.

        Attributes:
            id (int): Identifiant unique de la catégorie.
            name (str): Nom de la catégorie.
        """
        __tablename__ = "categorie"
        __table_args__ = {"extend_existing": True}

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)

        article = db.relationship('Article', back_populates='categorie')

    # Modèle de la classe sujet pour le forum.
    class SubjectForum(db.Model):
        """
        Modèle de données représentant un sujet pour le forum.

        Attributes:
            id (int): Identifiant unique du sujet pour le forum.
            nom (str): Nom du sujet du forum (limité à 50 caractères).
        """
        __tablename__ = "subject_forum"
        __table_args__ = {"extend_existing": True}

        id = db.Column(db.Integer, primary_key=True)
        nom = db.Column(db.String(50), nullable=False)

    # Modèle de la classe Comment pour les articles.
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
        replies_suppress_article = db.relationship('ReplyArticle', backref='parent_comment',
                                                   cascade='all, delete-orphan')

        # Relation avec la classe LikeCommentArticle avec suppression en cascade.
        likes_suppress_article = db.relationship('CommentLikeArticle', backref='comment_like_article',
                                                 cascade='all, delete-orphan')

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
        subject = db.relationship('SubjectForum', backref=db.backref('subject_comments', lazy=True))

        # Relation avec la classe User.
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        user = db.relationship('User', backref=db.backref('user_subject_comments', lazy=True))

        # Relation avec la classe ReplySubject avec suppression en cascade.
        replies_suppress_subject = db.relationship('ReplySubject', backref='parent_comment',
                                                   cascade='all, delete-orphan')

        # Relation avec la classe LikeCommentSubject avec suppression en cascade.
        likes_suppress_subject = db.relationship('CommentLikeSubject', backref='comment_like_subject',
                                                 cascade='all, delete-orphan')

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
        biography_mangaka = db.relationship('BiographyMangaka', backref=db.backref('biography_comments', lazy=True))

        # Relation avec la classe User.
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        user = db.relationship('User', backref=db.backref('user_biography_comments', lazy=True))

        # Relation avec la classe ReplyBiography avec suppression en cascade.
        replies_suppress_biography = db.relationship('ReplyBiography', backref='parent_comment',
                                                     cascade='all, delete-orphan')

        # Relation avec la classe LikeCommentBiography avec suppression en cascade.
        likes_suppress_biography = db.relationship('CommentLikeBiography', backref='comment_like_biography',
                                                   cascade='all, delete-orphan')

    # Table de liaison pour les likes.
    class Likes(db.Model):
        """
        Modèle de données représentant la relation entre les utilisateurs et les articles qu'ils aiment.

        Attributes:
            user_id (int) : Identifiant de l'utilisateur qui a aimé l'article (clé primaire).
            article_id (int): Identifiant de l'article aimé (clé primaire).
        """

        __tablename__ = "likes"
        __table_args__ = {"extend_existing": True}

        user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
        article_id = db.Column(db.Integer, db.ForeignKey("article.id", ondelete="CASCADE"), primary_key=True)

    # Table de liaison pour les dislikes.
    class Dislikes(db.Model):
        """
            Modèle de données représentant la relation entre les utilisateurs et les articles qu'ils n'aiment pas.

            Attributes:
                user_id (int) : Identifiant de l'utilisateur qui n'a pas aimé l'article (clé primaire).
                article_id (int): Identifiant de l'article désaimé (clé primaire).
        """
        __tablename__ = "dislikes"
        __table_args__ = {"extend_existing": True}

        user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
        article_id = db.Column(db.Integer, db.ForeignKey("article.id", ondelete="CASCADE"), primary_key=True)

    # Table de liaison pour les likes de la section biographie.
    class LikesBiography(db.Model):
        """
        Modèle de données représentant la relation entre les utilisateurs et les biographies qu'ils aiment.

        Attributes:
            user_id (int) : Identifiant de l'utilisateur qui a aimé la biographie (clé primaire).
            article_id (int): Identifiant de la biographie aimé (clé primaire).
        """

        __tablename__ = "likes_biography"
        __table_args__ = {"extend_existing": True}

        user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
        biography_mangaka_id = db.Column(db.Integer, db.ForeignKey("biography_mangaka.id", ondelete="CASCADE"),
                                         primary_key=True)

    # Table de liaison pour les dislikes de la section biographie.
    class DislikesBiography(db.Model):
        """
            Modèle de données représentant la relation entre les utilisateurs et les biographies qu'ils n'aiment pas.

            Attributes:
                user_id (int) : Identifiant de l'utilisateur.
                biography_mangaka_id (int) : Identifiant de la biographie.
            """
        __tablename__ = "dislikes_biography"
        __table_args__ = {"extend_existing": True}

        user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
        biography_mangaka_id = db.Column(db.Integer, db.ForeignKey("biography_mangaka.id", ondelete="CASCADE"),
                                         primary_key=True)

    # Table de liaison pour les likes des commentaires de la section article.
    class CommentLikeArticle(db.Model):
        """
        Modèle de données représentant la relation entre les utilisateurs et les commentaires
        qu'ils aiment dans la section article.

        Attributes:
            user_id (int) : Identifiant de l'utilisateur qui a aimé le commentaire (clé primaire).
            comment_id (int): Identifiant du commentaire aimé (clé primaire).
        """
        __tablename__ = "likes_comment_article"
        __table_args__ = {"extend_existing": True}

        user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
        comment_id = db.Column(db.Integer, db.ForeignKey("comment_article.id"), primary_key=True)

    # Table de liaison pour les likes des commentaires de la section forum.
    class CommentLikeSubject(db.Model):
        """
        Modèle de données représentant la relation entre les utilisateurs et les commentaires
        qu'ils aiment dans la section forum.

        Attributes:
            user_id (int) : Identifiant de l'utilisateur qui a aimé le commentaire (clé primaire).
            comment_id (int): Identifiant du commentaire aimé (clé primaire).
        """
        __tablename__ = "likes_comment_subject"
        __table_args__ = {"extend_existing": True}

        user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
        comment_id = db.Column(db.Integer, db.ForeignKey("comment_subject.id"), primary_key=True)

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

    # Table des réponses aux commentaires des articles.
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
        comment = db.relationship('CommentArticle', backref=db.backref('replies_comment_article', lazy=True))

        # Relation avec la classe User.
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        user = db.relationship('User', backref=db.backref('user_comment_article_replies', lazy=True))

    # Table des réponses aux commentaires des sujets du forum.
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
        comment = db.relationship('CommentSubject', backref=db.backref('replies_comment_subject', lazy=True))

        # Relation avec la classe User.
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        user = db.relationship('User', backref=db.backref('user_comment_subject_replies', lazy=True))

    # Table des réponses aux commentaires des biographies.
    class ReplyBiography(db.Model):
        """
        Représente une réponse à un commentaire sur une biographie.

        Attributes:
            id (int): Identifiant unique de la réponse.
            reply_content (str): Contenu de la réponse.
            reply_date (date): Date de la réponse.
            comment_id (int): Identifiant du commentaire associé à la réponse.
            user_id (int) : Identifiant de l'utilisateur ayant posté la réponse.
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


    # Création de toutes les tables à partir de leur classe.
    db.create_all()

print("Félicitations, toutes vos tables ont été installées.")

