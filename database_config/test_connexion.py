
"""
Script de connexion à la base de données PostgreSQL du blog.

Ce script se connecte à la base de données PostgreSQL du blog en utilisant la bibliothèque psycopg2.
Il récupère ensuite la version de PostgreSQL et affiche le résultat.
Enfin, il se déconnecte proprement de la base de données.

Paramètres de connexion à la base de données :
    - user : Le nom d'utilisateur utilisé pour se connecter à la base de données.
    - password : Le mot de passe associé à l'utilisateur pour l'authentification.
    - host : L'adresse IP ou le nom d'hôte de la machine où PostgreSQL est installé.
    - port : Le numéro de port sur lequel PostgreSQL écoute les connexions.
    - database : Le nom de la base de données à laquelle se connecter.

Exemple d'utilisation :
    python test_connexion.py

Ce script doit être exécuté sur le serveur où la base de données PostgreSQL est installée et accessible.
"""

import psycopg2

try:
    conn = psycopg2.connect(
        user="postgres",
        password="Monolithe8",
        host="localhost",
        port="5432",
        database="db_monblogmanga"
    )

    # Création du curseur pour agir sur la bade de données.
    cur = conn.cursor()

    # Affichage de la version de PostgreSQL.
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("Version :", version, "\n")

    # Déconnexion à la base de données.
    cur.close()
    conn.close()
    print("La connexion a bien été fermée")

# Renvoi d'une erreur si problème.
except (Exception, psycopg2.Error) as error:
    print("Erreur lors de la connexion à la base de donnée PostgreSQL", error)
