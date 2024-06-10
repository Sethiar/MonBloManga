"""Fichier app.py de lancement de mon blog"""

from datetime import datetime

from app import create_app

from flask import render_template, redirect, url_for


from app.Models.author import Author
from app.Models.articles import Article

from login_manager import login_manager

app = create_app()


# Route renvoyant l'erreur 404.
@app.errorhandler(404)
def page_not_found(error):
    """
    Renvoie une page d'erreur 404 en cas de page non trouvée.

    Args :
        error : L'erreur qui a déclenché la page non trouvée.

    Returns :
        La page d'erreur 404.
    """
    return render_template("Error/404.html"), 404


# Route permettant de renvoyant l'utilisateur vers les bons moyens d'authentification.
@login_manager.unauthorized_handler
def unauthorized():
    """
    Fonction exécutée lorsque l'utilisateur tente d'accéder à une page nécessitant une connexion,
    mais n'est pas authentifié. Redirige l'utilisateur vers la page "connexion_requise".

    Cette fonction est utilisée pour gérer les tentatives d'accès non autorisé à des pages nécessitant une connexion.
    Lorsqu'un utilisateur non authentifié essaie d'accéder à une telle page, cette fonction est appelée et redirige
    l'utilisateur vers la page "connexion_requise" où il peut se connecter.

    Returns:
        Redirige l'utilisateur vers la page "connexion_requise".
    """
    return redirect(url_for('functional.connexion_requise'))


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
