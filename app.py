"""Fichier app.py de lancement de mon blog"""
from datetime import datetime

from app.create_app import create_app

from flask import render_template

from Models.author import Author
from Models.articles import Article

app, login_manager, db = create_app()


# Route permettant d'accéder à l'accueil du blog.
@app.route("/")
def landing_page():
    """
    Page d'accueil de mon blog.

    Cette fonction renvoie la page d'accueil du blog. La page d'accueil est la première page
    que les utilisateurs voient lorsqu'ils accèdent au blog. Elle peut contenir des informations
    telles que des articles récents, des liens vers d'autres sections du blog, des catégories
    d'articles, etc.

    Returns :
        La page d'accueil du blog.
    """
    # Récupération de la date du jour.
    current_date = datetime.now().strftime("%d-%m-%Y")

    # Récupération de tous les articles et des auteurs depuis la base de données.
    articles = Article.query.all()
    authors = Author.query.all()
    return render_template("Presentation/accueil.html", articles=articles, authors=authors, current_date=current_date)

if __name__ == '__main__':
    app.run(debug=True)
