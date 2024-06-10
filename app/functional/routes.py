"""
Code permettant de définir les routes concernant les fonctions cachées, erreurs, logging, mentions légales ou
politique du blog.
"""

import uuid

from flask import render_template, session
from flask_login import current_user

from app.functional import functional_bp


def generate_unique_id():
    """Génère un identifiant unique pour les utilisateurs anonymes.
    Returns:
        str: L'identifiant unique est généré.
        """
    return str(uuid.uuid4())


# Route permettant à l'utilisateur de bien se connecter au blog.
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
    return render_template("Error/connexion_requise.html")


# Route permettant de valider une connexion ou d'en infirmer l'authenticité.
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


#  Route permettant d'accéder à la politique de confidentialité.
@functional_bp.route("/Politique_de_confidentialité")
def politique():
    """
    Accès à la Politique de confidentialité du blog.

    Returns :
        Redirige vers la page de politique de confidentialité du blog.
    """
    return render_template("Functional/politique.html")


#  Route permettant d'accéder aux mentions légales.
@functional_bp.route("/mentions_légales")
def mentions():
    """
    Accès aux Mentions légales du blog.
    Returns :
        Redirige vers la page de politique de confidentialité du blog.
    """
    return render_template("Functional/mentions.html")

