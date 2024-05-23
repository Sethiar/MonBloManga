"""

"""

import uuid

from flask import render_template, redirect, url_for, session
from flask_login import current_user

from login_manager import login_manager

from app.functional import functional_bp

def generate_unique_id():
    """Génère un identifiant unique pour les utilisateurs anonymes.
    Returns:
        str: L'identifiant unique est généré.
        """
    return str(uuid.uuid4())

@functional_bp.errorhandler(401)
def acces_no_autorise(error):
    """
    Renvoie une page d'erreur 401 en cas d'accès non autorisé.

    Args :
        error : L'erreur qui a déclenché l'accès non autorisé.

    Returns :
        La page d'erreur 401.
    """
    return render_template("functional/401.html")


@functional_bp.errorhandler(404)
def page_not_found(error):
    """
    Renvoie une page d'erreur 404 en cas de page non trouvée.

    Args :
        error : L'erreur qui a déclenché la page non trouvée.

    Returns :
        La page d'erreur 404.
    """
    return render_template("functional/404.html")


@login_manager.unauthorized_handler
def unauthorized():
    """
    Fonction exécutée lorsque l'utilisateur tente d'accéder à une page nécessitant une connexion,
    mais n'est pas authentifié. Redirige l'utilisateur vers la page "connexion_requise".

    Cette fonction est utilisée pour gérer les tentatives d'accès non autorisé à des pages nécessitant une connexion.
    Lorsqu'un utilisateur non authentifié essaie d'accéder à une telle page, cette fonction est appelée et redirige
    l'utilisateur vers la page "connexion_requise" où il peut se connecter.

    Returns:
        Redirige l'utilisateur vers la page "connexion_requise".
    """
    return redirect(url_for('functional.connexion_requise'))


@functional_bp.route("/connexion_requise")
def connexion_requise():
    """
    Route affichant un message informant l'utilisateur qu'une connexion est requise
    pour accéder à la page demandée.

    Cette route est utilisée pour informer l'utilisateur qu'une connexion est nécessaire
    pour accéder à une certaine page. Lorsqu'un utilisateur tente d'accéder à une page
    nécessitant une connexion mais n'est pas authentifié, il est redirigé vers cette page
    où un message lui indique qu'il doit d'abord se connecter.

    Returns:
        Le template HTML de la page "connexion_requise".
    """
    return render_template("functional/connexion_requise.html")


@functional_bp.before_request
def before_request():
    """
    Ce code permet de gérer les connexions des utilisateurs et des anonymes.
    """
    if current_user.is_authenticated:
        pseudo = current_user.pseudo
        session['pseudo'] = pseudo
    else:
        session['anon_id'] = generate_unique_id()


@functional_bp.route("/Politique_de_confidentialité")
def politique():
    """
    Accès à la Politique de confidentialité du blog.

    Returns :
        Redirige vers la page de politique de confidentialité du blog.
    """
    return render_template("functional/politique.html")


@functional_bp.route("/mentions_légales")
def mentions():
    """
    Accès aux Mentions légales du blog.
    Returns :
        Redirige vers la page de politique de confidentialité du blog.
    """
    return render_template("functional/mentions.html")

