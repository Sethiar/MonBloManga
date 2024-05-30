"""
Représente la classe des commentaires des sujets du forum.
"""

from . import db
from datetime import datetime


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

    # Comptage des likes.
    likes = db.Column(db.Integer, nullable=False, default=0)

    # Relation avec la classe SubjectForum.
    subject_id = db.Column(db.Integer, db.ForeignKey('subject_forum.id'), nullable=False)
    subject = db.relationship('SubjectForum', backref=db.backref('comments', lazy=True))

    # Relation avec la classe User.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('subject_comments', lazy=True))

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet Comment.

        Returns :
            str: Chaîne représentant l'objet Comment.
        """
        return f"CommentSubject(id={self.id}, subject_id={self.subject_id}, user_id={self.user_id}, " \
               f"date={self.comment_date}, like={self.likes})"
