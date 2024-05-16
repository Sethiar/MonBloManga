
"""
Déclaration de la table de données.

Cette section définit la structure de la table de données utilisée dans l'application. La table de données est généralement une représentation des entités métier de votre application, telles que les utilisateurs, les produits, les commandes, etc.

L'utilisation de SQLAlchemy simplifie l'interaction avec la base de données en permettant de définir les modèles de données sous forme de classes Python.

Exemple d'utilisation :
    # Définition d'un modèle utilisateur
    class User(db.Model):
        __tablename__ = 'users'

        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)

        def __repr__(self):
            return f"<User {self.username}>"

    # Création de la table dans la base de données
    db.create_all()

Cette déclaration de table de données utilise SQLAlchemy, un ORM (Object-Relational Mapping) pour la gestion de la base de données dans Flask. SQLAlchemy permet de définir les structures de données de manière intuitive à l'aide de classes Python, qui sont ensuite traduites en schémas de base de données.

Pour en savoir plus sur la manière de définir des modèles de données avec SQLAlchemy, consultez la documentation officielle : https://docs.sqlalchemy.org/en/14/orm/tutorial.html
"""


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
