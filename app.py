"""Fichier app.py de lancement de mon blog"""

from datetime import datetime

from app import create_app

from flask import render_template, redirect, url_for
from calendar import month_name


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
    articles = Article.query.order_by(Article.date_edition.desc()).all()
    authors = Author.query.all()

    # Division des articles en new_articles et other_articles.
    new_articles = articles[:2]
    other_articles = articles[2:8]

    # Générer la liste des mois d'archive
    archive_months = []

    # Définir la date de début pour les archives
    start_year = 2024
    start_month = 4

    # Récupérer la date actuelle
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Boucle pour générer les années
    for year in range(start_year, current_year + 1):
        # Boucle pour générer les mois
        # Si l'année est celle en cours, arrêter au mois actuel
        if year == current_year:
            end_month = current_month
        else:
            end_month = 12  # Sinon, générer jusqu'à décembre
        for month in range(start_month, end_month + 1):
            archive_months.append((year, month, month_name[month]))

    return render_template(
        "Presentation/accueil.html", new_articles=new_articles, other_articles=other_articles,
        archive_months=archive_months, current_date=current_date)


if __name__ == '__main__':
    app.run(debug=True)
