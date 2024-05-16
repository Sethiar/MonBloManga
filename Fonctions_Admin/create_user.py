"""
Ce script crée un utilisateur pour le blog.

Il enregistre les informations de l'auteur dans la base de données.
Il faut s'assurer d'avoir configuré la connexion à la base de données correctement et d'avoir les autorisations nécessaires pour insérer des données.

Exemple d'utilisation :
    python create_user.py
"""
import sys
import os
import bcrypt


# Chemin absolu du répertoire courant
current_dir = os.path.abspath(os.path.dirname(__file__))

# Chemin absolu du répertoire parent
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Ajouter le répertoire parent au sys.path
sys.path.append(parent_dir)


# Importer la fonction conn() depuis db_monblogmanga.py
from database_config.db_monblogmanga import conn

# Si vous voulez changer votre identifiant et votre mot de passe, c'est ici'
pseudo = "Nosiris"
email = "lefeteyarnaud@gmail.com"
date_naissance = "08/06/1983"
password = "Monolithe8"
banned = False

# Génération d'un sel aléatoire pour le hachage du mot de passe.
salt = bcrypt.gensalt()

# Hachage du mot de passe avec le sel généré.
password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

print("Le processus de hachage a bien fonctionné.")

# Sélection d'un curseur pour action sur la base de données.
cur = conn.cursor()

# Insertion de l'identifiant et du mot de passe hashé dans la base de données.
cur.execute(
    "INSERT INTO user(pseudo, email, date_naissance, password_hash, salt, banned) VALUES (%s, %s, %s, %s, %s, %s)",
    (pseudo, email, date_naissance, password_hash, salt, banned)
)
print("Les identifiants de l'utilisateur ont bien été enregistrés dans la base de données.")

# Validation de la procédure et enregistrement au sein de la base de données.
conn.commit()

# Génération d'un message affirmant que la procédure s'est bien passée.
print("Les identifiants de l'utilisateur ont bien été enregistrés et sont sécurisés.")

