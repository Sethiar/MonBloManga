"""Fichier app.py de lancement de mon blog"""

from app.create_app import create_app

app, login_manager, db = create_app()


if __name__ == '__main__':
    app.run(debug=True)
