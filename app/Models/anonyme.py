"""Code de la classe Anonyme."""

from flask_login import AnonymousUserMixin


class Anonyme(AnonymousUserMixin):
    """
    Classe représentant un utilisateur anonyme.

    Cette classe est utilisée pour représenter un utilisateur non authentifié
    dans le système.

    Attributes :
        Aucun attribut défini explicitement.
    """

    def __init__(self):
        """
        Initialise un utilisateur anonyme.

        Il n'y a pas d'attributs à initialiser pour un utilisateur anonyme.
        """

    def is_authenticated(self):
        """
        Vérifie si l'utilisateur est authentifié.

        Returns :
            bool: False, car l'utilisateur n'est pas authentifié.
        """
        # L'utilisateur anonyme n'est pas authentifié
        return False

    def is_active(self):
        """
        Vérifie si l'utilisateur est actif.

        Returns :
             bool : True car l'utilisateur est considéré comme actif.
        """
        # L'utilisateur anonyme est considéré comme actif
        return True


