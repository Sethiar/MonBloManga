"""
Code permettant de définir les routes concernant les fonctions cachées du blog.
"""

from flask import Blueprint

functional_bp = Blueprint('functional', __name__)

from app.functional import routes

