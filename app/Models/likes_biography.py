"""Classe représentant les likes et les dislikes pour les biographies pour les utilisateurs du blog."""

from . import db


# Table de liaison pour les likes de la section biographie.
class LikesBiography(db.Model):
    """
    Modèle de données représentant la relation entre les utilisateurs et les biographies qu'ils aiment.

    Attributes:
        user_id (int) : Identifiant de l'utilisateur.
        biography_mangaka_id (int) : Identifiant de la biographie.
    """

    __tablename__ = "likes_biography"
    __table_args__ = {"extend_existing": True}

    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"),  primary_key=True)
    biography_mangaka_id = db.Column(db.Integer, db.ForeignKey("biography_mangaka.id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet LikesBiography.

        Returns :
            str: Chaîne représentant l'objet LikesBiography.
        """
        return f"LikesBiography(user_id='{self.user_id}', biography_mangaka_id='{self.biography_mangaka_id}')"


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
    biography_mangaka_id = db.Column(db.Integer, db.ForeignKey("biography_mangaka.id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        return f"DislikesBiography(user_id='{self.user_id}', biography_mangaka_id='{self.biography_mangaka_id}')"

