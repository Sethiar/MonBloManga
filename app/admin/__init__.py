"""
Initialisation du module admin.

Ce fichier configure le Blueprint pour les routes d'administration et importe les routes associées.
"""

from flask import Blueprint

# Création du Blueprint pour le module admin
admin_bp = Blueprint('admin', __name__)

# Importation des routes associées au Blueprint admin
from app.admin import routes