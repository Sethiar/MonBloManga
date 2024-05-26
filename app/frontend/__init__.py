"""
Code permettant de définir les routes concernant le frontend du blog.

"""

from flask import Blueprint

frontend_bp = Blueprint('frontend', __name__)

from app.frontend import routes
