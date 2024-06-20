"""
Code permettant de définir les routes concernant les fonctions cachées, erreurs, logging, mentions légales ou
politique du blog.
"""

import uuid

from flask import render_template, session
from flask_login import current_user

from app.functional import functional_bp


def generate_unique_id():
    """
    Génère un identifiant unique au format UUID pour les utilisateurs anonymes.

    Returns:
        str: Identifiant unique généré au format UUID.
    """
    return str(uuid.uuid4())


# Route permettant à l'utilisateur de bien se connecter au blog.
@functional_bp.route("/connexion_requise")
def connexion_requise():
    """
    Route affichant un message informant l'utilisateur qu'une connexion est requise
    pour accéder à la page demandée.

    Cette route redirige les utilisateurs non authentifiés vers une page indiquant
    qu'ils doivent se connecter pour accéder à la ressource demandée.

    Returns:
        Le template HTML de la page "connexion_requise".
    """
    return render_template("Error/connexion_requise.html")


# Route permettant de valider une connexion ou d'en infirmer l'authenticité.
@functional_bp.before_request
def before_request():
    """
    Fonction exécutée avant chaque requête vers les routes de ce blueprint.

    Gère les sessions utilisateur en fonction de leur statut d'authentification :
    - Si l'utilisateur est authentifié, enregistre son pseudo dans la session.
    - Si l'utilisateur n'est pas authentifié, génère un identifiant unique pour les utilisateurs anonymes
      et l'enregistre dans la session.

    Cette fonction assure la continuité de la session utilisateur à travers le site.
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

    Returns:
        Template HTML de la page de politique de confidentialité du blog.
    """
    return render_template("Functional/politique.html")


#  Route permettant d'accéder aux mentions légales.
@functional_bp.route("/mentions_légales")
def mentions():
    """
    Accès aux Mentions légales du blog.

    Returns:
        Template HTML de la page de mentions légales du blog.
    """
    return render_template("Functional/mentions.html")

