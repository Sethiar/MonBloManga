"""Code de la classe Anonyme."""

from flask_login import AnonymousUserMixin


class Anonyme(AnonymousUserMixin):
    """
    Classe représentant un utilisateur anonyme.
    """

    def __init__(self):
        """
        Initialisation d'un utilisateur anonyme.
        """

    def is_authentificated(self):
        """
        Vérifie si l'utilisateur est authentifié.

        Returns:
            bool: False, car l'utilisateur n'est pas authentifié.
        """
        # L'utilisateur anonyme n'est pas authentifié
        return False

    def is_active(self):
        """
        Vérifie si l'utilisateur est actif.

        Returns:
             bool: True car l'utilisateur est considéré comme actif.
        """
        # L'utilisateur anonyme est considéré comme actif
        return True

