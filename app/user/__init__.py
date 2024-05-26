"""
Code permettant de définir les routes utilisées par les utilisateurs du blog.
"""

from flask import Blueprint

user_bp = Blueprint('user', __name__)

from app.user import routes
