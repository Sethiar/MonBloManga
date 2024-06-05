
"""
Déclaration de la table de données.

Cette section définit la structure de la table de données utilisée dans l'application. La table de données est
généralement une représentation des entités métier de votre application, telles que les utilisateurs, les produits,
les commandes, etc.

L'utilisation de SQLAlchemy simplifie l'interaction avec la base de données en permettant de définir
les modèles de données sous forme de classes Python.

Cette déclaration de table de données utilise SQLAlchemy, un ORM (Object-Relational Mapping) pour la gestion de
la base de données dans Flask. SQLAlchemy permet de définir les structures de données de manière intuitive à l'aide de
classes Python, qui sont ensuite traduites en schémas de base de données.

"""


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

