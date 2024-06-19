"""
Modèle de la table de données enregistrant les mangakas.
"""
from . import db
from datetime import datetime


# Table de données concernant les biographies des mangakas.
class BiographyMangaka(db.Model):
    """
    Table de données qui enregistre les biographies des mangakas.

    Attributes :
        id (int) : identifiant unique de la table.
        biography_content (str) : Contenu de la biographie.
        date_bio_mangaka (date) : Date d'édition de la biographie.
        mangaka_name (str) : Nom du mangaka.
        pseudo_author (str) : pseudo de l'auteur de la biographie.

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

    # Enregistrement des likes et dislikes des biographies.
    likes = db.Column(db.Integer, nullable=False, default=0)
    dislikes = db.Column(db.Integer, nullable=False, default=0)

    # Ajout de la relation avec suppression en cascade pour les commentaires.
    comments = db.relationship('CommentBiography', backref='comment_biography', cascade='all, delete-orphan')

    # Ajout des relations avec suppression en cascade pour les likes et dislikes.
    likes_rel = db.relationship('LikesBiography', backref='liked_biography',
                                cascade='all, delete-orphan', lazy='dynamic')
    dislikes_rel = db.relationship('DislikesBiography', backref='disliked_biography',
                                   cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet biography_mangaka.

        Returns :
            str: Chaîne représentant biography_mangaka.
        """
        return f"BiographyMangaka(nom_mangaka='{self.mangaka_name}', Auteur='{self.author.pseudo}', " \
               f"Date d'édition='{self.date_bio_mangaka}', Biographie_contenu='{self.biography_content}')" \
               f"like='{self.likes}', dislikes='{self.dislikes}')"

