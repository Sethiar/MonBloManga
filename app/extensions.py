"""
Code source qui permet d'initialiser les extensions.
"""

# Fonctions vérifiant les extensions des imports.
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    """
    Vérifie si l'extension d'un fichier est autorisée en fonction de la liste ALLOWED_EXTENSIONS.

    :param filename: Nom du fichier à vérifier.
    :return: True si l'extension est autorisée, False sinon.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


