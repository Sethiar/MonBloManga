"""
Initialisation du module auth.

Ce fichier configure le Blueprint pour les routes d'authentification et importe les routes associées.
"""

from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from app.auth import routes
