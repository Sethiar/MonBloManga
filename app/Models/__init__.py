
"""
Déclaration de la base de données.

Cette instance `db` permet de représenter la connexion à la base de données et fournit des méthodes pour interagir
avec les tables de données définies par les modèles SQLAlchemy.
"""

from flask_sqlalchemy import SQLAlchemy

# Instanciation de la base de données.
db = SQLAlchemy()

