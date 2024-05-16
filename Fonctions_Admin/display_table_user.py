"""
Script permettant d'afficher les données de la table user du blog.

Ce script se connecte à la base de données et affiche les informations des administrateurs enregistrés dans la table admin.

Il faut s'assurer d'avoir configuré correctement la connexion à la base de données et d'avoir les autorisations nécessaires pour effectuer des opérations de lecture.

Exemple d'utilisation :
    python display_table_user.py
"""

import sys
import os

# Chemin absolu du répertoire courant.
current_dir = os.path.abspath(os.path.dirname(__file__))

# Chemin absolu du répertoire parent.
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Ajouter le répertoire parent au sys.path.
sys.path.append(parent_dir)

from database_config.db_monblogmanga import conn

# Initialisation du curseur.
cur = conn.cursor()

# Exécution d'une requête de sélection.
cur.execute("SELECT nom, prenom, date_naissance, email, genre FROM user")

# Récupération des résultats de la requête.
rows = cur.fetchall()

# Affichage des résultats.
for row in rows:
    print("nom : ", row[0])
    print("prénom :", row[1])
    print("date de naissance :", row[2])
    print("email :", row[3])

# Fermeture de la connexion.
cur.close()
conn.close()
