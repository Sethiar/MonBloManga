"""
Ce script crée un auteur pour le blog.

Il enregistre les informations de l'auteur dans la base de données.
Il faut s'assurer d'avoir configuré la connexion à la base de données correctement et d'avoir les autorisations nécessaires pour insérer des données.

Exemple d'utilisation :
    python create_author.py
"""

import sys
import os

# Chemin absolu du répertoire courant
current_dir = os.path.abspath(os.path.dirname(__file__))

# Chemin absolu du répertoire parent
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Ajouter le répertoire parent au sys.path
sys.path.append(parent_dir)

# Importer la fonction conn() depuis db_monblogmanga.py
from database_config.db_monblogmanga import conn


# Infos test.
nom = "Lefetey"
prenom = "Arnaud"
pseudo = "Nosiris"


# Sélection d'un curseur pour action sur la base de données.
cur = conn.cursor()

# Enregistrement des informations de l'auteur.
cur.execute(
    "INSERT INTO author(nom, prenom, pseudo) VALUES (%s, %s, %s)",
    (nom, prenom, pseudo)
)

# Validation de la procédure et enregistrement au sein de la base de données.
conn.commit()

# Génération d'un message affirmant que la procédure s'est bien passée.
print("L'auteur a bien été enregistré.")
