"""Ce script configure la connexion à la base de données du blog.

Il se connecte à la base de données PostgreSQL 'db_monblogmanga' en utilisant les paramètres spécifiés
(user, password, host, port, database). Ensuite, il crée un curseur pour effectuer des opérations sur la base de données.
Finalement, il affiche la version de la base de données PostgreSQL.

Assurez-vous que les paramètres de connexion sont corrects et que la base de données 'db_monblogmanga' existe sur le serveur PostgreSQL.

Exemple d'utilisation :
    python db_monblogmanga.py
"""

import psycopg2

# Paramètres de la base de données db_monblogmanga

conn = psycopg2.connect(
    user="postgres",
    password="Monolithe8",
    host="localhost",
    port="5432",
    database="db_monblogmanga"
    )

# Création du curseur pour pouvoir faire agir sur la database

cur = conn.cursor()


# Afficher la version de la base de PostgreSQL

cur.execute("SELECT version();")
version = cur.fetchone()
print("Version : ", version, "\n")
