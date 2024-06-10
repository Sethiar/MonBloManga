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
        mangaka_name (str) : Nom du mangaka.
    """
    __tablename__ = "biography_mangaka"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    biography_content = db.Column(db.Text(), nullable=False)

    # Date d'édition de la biographie.
    date_bio_mangaka = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Nom du mangaka.
    mangaka_name = db.Column(db.String(50), nullable=False)

    # Pseudo de l'auteur de l'article.
    pseudo_author = db.Column(db.String(30), db.ForeignKey('author.pseudo'), nullable=True)

    # Relation avec la classe Author.
    author = db.relationship('Author', backref=db.backref('biography_mangaka', lazy=True))

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet biography_mangaka.

        Returns :
            str: Chaîne représentant biography_mangaka.
        """
        return f"BiographyMangaka(nom_mangaka='{self.mangaka_name}', Auteur='{self.author.pseudo}', " \
               f"Date d'édition='{self.date_bio_mangaka}', Biographie_contenu='{self.biography_content}')"
