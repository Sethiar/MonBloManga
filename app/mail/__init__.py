"""
Code permettant de définir les routes concernant le mailing du blog.
"""

from flask import Blueprint

mail_bp = Blueprint('mail', __name__)

from app.mail import routes



