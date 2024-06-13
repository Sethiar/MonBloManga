"""
Script permettant de supprimer les données de la table biography_mangaka du blog.

Ce script se connecte à la base de données et supprime les informations des biographies enregistrées
dans la table biography_mangaka.

Il faut s'assurer d'avoir configuré correctement la connexion à la base de données et d'avoir les autorisations
nécessaires pour effectuer des opérations de lecture.

Exemple d'utilisation :
    python suppress_subject.py
"""

import sys
import os


# Chemin absolu du répertoire courant
current_dir = os.path.abspath(os.path.dirname(__file__))

# Chemin absolu du répertoire parent
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Ajouter le répertoire parent au sys.path
sys.path.append(parent_dir)

# Importer la fonction conn() depuis db_monblogmanga .py
from database_config.db_monblogmanga import conn

# Création d'un curseur
cur = conn.cursor()

# Exécution d'une requête de suppression
cur.execute("DELETE FROM biography_mangaka")

# Validation de la transaction
conn.commit()
print('Toutes les données de la table biography_mangaka ont bien été supprimées.')

# Fermeture de la connexion
cur.close()
conn.close()
