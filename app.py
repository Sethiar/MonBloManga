"""Fichier app.py de lancement de mon blog"""

import bcrypt

from datetime import datetime

from flask import render_template, url_for, request, \
    redirect, flash, session, abort, jsonify

from flask_login import login_required, current_user, login_user, \
    logout_user
from markupsafe import escape

from Models.admin import Admin
from Models.user import User
from Models.articles import Article
from Models.author import Author
from Models.categories_articles import Categorie
from Models.subjects_forum import SubjectForum
from Models.comment import Comment
from Models.reply import Reply

from Models.forms import AdminConnection
from Models.forms import NewCategorieForm, NewSubjectForumForm, ArticleForm, \
    UserSaving, CommentForm, NewAuthor, LikeForm, DislikeForm,ReplyForm
from Models.forms import UserConnection

from create_app import create_app, generate_unique_id

app, login_manager, db = create_app()


@app.errorhandler(401)
def acces_no_autorise(error):
    """
    Renvoie une page d'erreur 401 en cas d'accès non autorisé.

    Args :
        error : L'erreur qui a déclenché l'accès non autorisé.

    Returns :
        La page d'erreur 401.
    """
    return render_template("Fonctional/401.html")


@app.errorhandler(404)
def page_not_found(error):
    """
    Renvoie une page d'erreur 404 en cas de page non trouvée.

    Args :
        error : L'erreur qui a déclenché la page non trouvée.

    Returns :
        La page d'erreur 404.
    """
    return render_template("Fonctional/404.html")


@login_manager.unauthorized_handler
def unauthorized_callback():
    """
    Fonction exécutée lorsque l'utilisateur tente d'accéder à une page nécessitant une connexion,
    mais n'est pas authentifié. Redirige l'utilisateur vers la page "connexion_requise".

    Cette fonction est utilisée pour gérer les tentatives d'accès non autorisé à des pages nécessitant une connexion.
    Lorsqu'un utilisateur non authentifié essaie d'accéder à une telle page, cette fonction est appelée et redirige
    l'utilisateur vers la page "connexion_requise" où il peut se connecter.

    Returns:
        Redirige l'utilisateur vers la page "connexion_requise".
    """
    return redirect(url_for('connexion_requise'))


@app.route("/connexion_requise")
def connexion_requise():
    """
    Route affichant un message informant l'utilisateur qu'une connexion est requise
    pour accéder à la page demandée.

    Cette route est utilisée pour informer l'utilisateur qu'une connexion est nécessaire
    pour accéder à une certaine page. Lorsqu'un utilisateur tente d'accéder à une page
    nécessitant une connexion mais n'est pas authentifié, il est redirigé vers cette page
    où un message lui indique qu'il doit d'abord se connecter.

    Returns:
        Le template HTML de la page "connexion_requise".
    """
    return render_template("Fonctional/connexion_requise.html")


@app.before_request
def before_request():
    """
    Ce code permet de gérer les connexions des utilisateurs et des anonymes.
    """
    if current_user.is_authenticated:
        pseudo = current_user.pseudo
        session['pseudo'] = pseudo
    else:
        session['anon_id'] = generate_unique_id()


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


@app.route("/deconnexion", methods=["GET"])
def user_logout():
    """
    Déconnecte l'utilisateur actuellement authentifié et l'admin du système.

    Cette fonction gère la déconnexion des utilisateurs en supprimant les informations d'identification stockées dans la session Flask.

     Les sessions Flask sont un mécanisme permettant de stocker des données spécifiques à un utilisateur entre différentes requêtes HTTP.
     Dans ce cas, les informations d'identification telles que l'état de connexion, l'identifiant de l'utilisateur et l'identifiant de
     session sont stockées dans la session Flask lorsqu'un utilisateur se connecte avec succès. Cette fonction supprime ces informations de
     la session lorsqu'un utilisateur se déconnecte.

    Returns :
        redirige l'utilisateur vers la page accueil.html après la déconnexion.

    Notes :
        La déconnexion est effectuée en supprimant les clés de session "logged_in", "identifiant" et "user_id".
        Si aucun utilisateur n'est connecté, cette fonction n'a aucun effet et redirige simplement vers la page accueil.html.
    """
    # Supprime les informations d'identification de l'utilisateur de la session.
    session.pop("logged_in", None)
    session.pop("identifiant", None)
    session.pop("user_id", None)
    logout_user()

    # Redirige vers la page d'accueil après la déconnexion.
    return redirect(url_for('landing_page'))


@app.route("/articles", methods=['GET', 'POST'])
def reading_articles():
    """
    Route pour afficher tous les articles disponibles sur le blog.

    Returns:
        Template HTML contenant la liste des articles.

    Notes:
        Si la méthode HTTP est GET, la fonction récupère tous les articles de la base de données
        et les affiche dans le template HTML 'Presentation/articles.html'.
        Si la méthode HTTP est POST, la fonction valide le formulaire de commentaire soumis.
        Si le formulaire est valide, elle redirige l'utilisateur vers une autre page.
        Sinon, elle affiche la liste des articles avec les erreurs de formulaire.

    Raises:
        Aucune exception n'est levée.

    Examples:
        Exemple d'utilisation GET :
            L'utilisateur accède à la route /articles via un navigateur web.
            La fonction récupère tous les articles de la base de données et les affiche dans le template HTML.

        Exemple d'utilisation POST :
            L'utilisateur soumet un formulaire de commentaire avec des données valides.
            La fonction valide le formulaire, traite les données et redirige l'utilisateur vers une autre page.

    """
    form = CommentForm()

    if request.method == 'POST':
        # Validation du formulaire du commentaire.
        if form.validate_on_submit():
            # Récupération du pseudo de l'utilisateur depuis le formulaire.
            user_pseudo = form.pseudo_user.data
            return redirect(url_for("comment_article", user_pseudo=user_pseudo))
        else:
            # Si le formulaire n'est pas valide, affichage de la page des articles.
            articles = Article.query.all()
            authors = Author.query.all()
            return render_template("Presentation/articles.html", articles=articles, authors=authors, form=form,
                                   error="Veuillez saisir un pseudo valide.")

    else:
        # Si la méthode n'est pas POST, simple affichage.
        # Récupération de tous les articles et des auteurs depuis la base de données.
        articles = Article.query.all()
        authors = Author.query.all()
        return render_template("Presentation/articles.html", articles=articles, form=form, authors=authors)


@app.route("/article/<int:article_id>")
def show_article(article_id):
    """
    Route permettant d'afficher un article spécifique.

    Args:
        article_id (int): L'ID de l'article à afficher.

    Returns:
        Template HTML contenant les détails de l'article.

    Raises:
        404 Error: Si l'article avec l'ID spécifié n'est pas trouvé dans la base de données.

    Examples:
        Exemple d'utilisation :
            L'utilisateur accède à la route /article/<article_id> via un navigateur web.
            La fonction récupère l'article correspondant à l'ID spécifié depuis la base de données.
            Si l'article est trouvé, la fonction affiche ses détails dans le template HTML 'Presentation/article.html'.
            Si aucun article correspondant à l'ID n'est trouvé, la fonction renvoie une erreur 404.
    """

    # Création de l'instance du formulaire.
    formcomment = CommentForm()
    formlike = LikeForm()
    formdislike = DislikeForm()

    # Récupération de l'article depuis la base de données en utilisant son id.
    article = Article.query.get(article_id)

    # Vérifier si l'article existe.
    if not article:
        # Si l'article n'existe pas, renvoyer une erreur 404.
        abort(404)

    # Récupération des commentaires associés à cet article.
    comments = Comment.query.filter_by(article_id=article_id).all()

    return render_template("Presentation/article.html", article=article, article_id=article_id, comments=comments,
                           formcomment=formcomment, formlike=formlike, formdislike=formdislike)


@app.route("/article/likes<int:article_id>", methods=['POST'])
def article_like(article_id):
    """

    :param article_id:
    :return:
    """
    # Instanciation des formulaires.
    formlike = LikeForm()
    formdislike = DislikeForm()
    formcomment = CommentForm()

    if formlike.validate_on_submit():
        # Récupération des articles ou de l'error 404 si aucun article.
        article = Article.query.get_or_404(article_id)
        # Ajout d'un like.
        article.likes += 1
        # Récupération des commentaires de l'article.
        comments = Comment.query.filter_by(article_id=article_id).all()
        # Enregistrement dans la base de données.
        db.session.commit()
        # Redirection vers la page de l'article.
        return redirect(url_for('show_article', article_id=article_id))


@app.route("/article/dislikes<int:article_id>", methods=['POST'])
def article_dislike(article_id):
    """

    :param article_id:
    :return:
    """
    # Instanciation des formulaires.
    formdislike = DislikeForm()
    formlike = LikeForm()
    formcomment = CommentForm()

    if formdislike.validate_on_submit():
        # Récupération des articles ou de l'error 404 si aucun article.
        article = Article.query.get_or_404(article_id)
        # Ajout d'un dislike.
        article.dislikes += 1
        # Récupération des commentaires de l'article.
        comments = Comment.query.filter_by(article_id=article_id).all()
        # Enregistrement dans la base de données.
        db.session.commit()
    # Redirection vers la page de l'article.
    return redirect(url_for('show_article', article_id=article_id))

@app.route("/mangaka")
def mangaka():
    """
    Accès à la page de la biographie des mangakas.

    Returns :
    La page des Mangakas.
    """
    return render_template("Presentation/mangaka.html")


@app.route("/connexion_admin_form", methods=['GET', 'POST'])
def admin_connection():
    """
    Route permettant d'accéder au formulaire de connexion pour l'administrateur.

    Returns:
        Template HTML du formulaire de connexion administrateur.

    Description:
        Cette route affiche un formulaire de connexion spécifiquement conçu pour l'administrateur
        du système. Le formulaire permet à l'administrateur de saisir ses identifiants
        (nom d'utilisateur et mot de passe) afin d'accéder à son espace administrateur
        et de bénéficier de fonctionnalités réservées aux administrateurs.

    Example:
        L'administrateur accède à cette route via un navigateur web.
        La fonction renvoie le template HTML 'Admin/admin_connection.html' contenant le formulaire de connexion.
        L'administrateur saisit ses identifiants et soumet le formulaire pour se connecter à son espace administrateur.
    """
    # Création de l'instance du formulaire.
    form = AdminConnection()
    return render_template("Admin/admin_connection.html", form=form)


@app.route("/connexion_admin", methods=['GET', 'POST'])
def login_admin():
    """
    Gère l'authentification de l'administrateur pour accéder au back-end du blog.

    Cette route gère le processus d'authentification de l'administrateur afin de lui permettre d'accéder
    à l'interface back-end du blog. L'administrateur saisit son identifiant, son mot de passe et son rôle
    (par exemple, SuperAdmin) via un formulaire de connexion dédié.

    Returns:
        - Redirige l'administrateur vers la page back_end s'il est authentifié avec succès.
        - Redirige l'administrateur vers la page de connexion admin_connection si l'authentification échoue.

    Notes:
        - En cas de succès, les informations d'identification de l'administrateur sont stockées dans la session Flask
          pour maintenir sa connexion active.
        - En cas d'échec de l'authentification, l'administrateur est redirigé vers la page de connexion admin_connection
          avec un avertissement approprié.
        - Les journaux d'application sont utilisés pour enregistrer les tentatives de connexion réussies et les erreurs.

    Example:
        L'administrateur accède à la route '/connexion_admin' via un navigateur web.
        Il saisit ses informations d'identification (identifiant, mot de passe et rôle) dans le formulaire de connexion.
        Après soumission du formulaire, l'application vérifie les informations et authentifie l'administrateur.
        Si l'authentification réussit, l'administrateur est redirigé vers la page back_end du blog.
        Sinon, il est redirigé vers la page de connexion admin_connection avec un message d'erreur.
    """
    # Création de l'instance du formulaire.
    form = AdminConnection()

    if request.method == 'POST':
        if form.validate_on_submit():
            identifiant = form.identifiant.data
            password = form.password.data
            role = form.role.data

            # Validation de la connexion.
            admin = Admin.query.filter_by(identifiant=identifiant).first()
            if admin is not None and bcrypt.checkpw(password.encode('utf-8'), admin.password_hash):

                # Authentification réussie.
                if role == "SuperAdmin":
                    app.logger.info(f"L'administrateur {admin.identifiant} s'est bien connecté.")

                    # Connexion de l'admin et stockage de ses informations dans la session.
                    session["logged_in"] = True
                    session["identifiant"] = admin.identifiant
                    session["user_id"] = admin.id

                    return redirect(url_for("back_end"))
                else:
                    app.logger.warning(
                        f"L'administrateur {admin.identifiant} n'a pas le rôle de SuperAdmin, ses possibilités sont restreintes.")
            else:
                app.logger.warning(
                    f"Tentative de connexion échouée avec l'identifiant {identifiant}. Veuillez réessayer avec un autre identifiant.")
                return redirect(url_for("admin_connection"))

    return render_template("Admin/admin_connection.html", form=form)


@app.route("/back_end_blog/admin_deconnexion", methods=['GET'])
def admin_logout():
    """
    Déconnecte l'administrateur actuellement authentifié et l'admin du système.

    Cette fonction gère la déconnexion des administrateurs en supprimant les informations d'identification stockées dans la session Flask.

     Les sessions Flask sont un mécanisme permettant de stocker des données spécifiques à un utilisateur entre différentes requêtes HTTP.
     Dans ce cas, les informations d'identification telles que l'état de connexion, l'identifiant de l'utilisateur et l'identifiant de
     session sont stockées dans la session Flask lorsqu'un utilisateur se connecte avec succès. Cette fonction supprime ces informations de
     la session lorsqu'un utilisateur se déconnecte.

    Returns :
        redirige l'administrateur vers la page accueil.html après la déconnexion.

    Notes :
        La déconnexion est effectuée en supprimant les clés de session "logged_in", "identifiant" et "admin_id".
        Si aucun utilisateur n'est connecté, cette fonction n'a aucun effet et redirige simplement vers la page accueil.html.
    """
    # Supprime les informations d'identification de l'utilisateur de la session.
    session.pop("logged_in", None)
    session.pop("identifiant", None)
    session.pop("admin_id", None)
    logout_user()

    # Redirige vers la page d'accueil après la déconnexion.
    return redirect(url_for('landing_page'))


# Route utilisée pour accéder au back_end du blog.
@app.route("/back_end")
def back_end():
    """
    Route utilisée pour accéder au back-end du blog après l'authentification de l'administrateur.

    Cette route permet à l'administrateur d'accéder au back-end du blog une fois qu'il est authentifié.
    L'administrateur doit être connecté avec les informations d'identification valides pour accéder à cette page.
    Une fois authentifié, l'administrateur peut visualiser et gérer les enregistrements des catégories d'articles,
    les articles eux-mêmes, les auteurs, et les sujets du forum.

    Returns:
        - La page back-end du blog si l'administrateur est authentifié et connecté.
        - Redirige l'administrateur vers la page de connexion admin_connection si l'authentification échoue
          ou s'il n'est pas encore connecté.

    Notes:
        - La fonction vérifie d'abord si l'utilisateur est connecté en tant qu'administrateur en vérifiant
          la présence de la clé "logged_in" dans la session Flask et sa valeur.
        - Si l'utilisateur est authentifié, la fonction récupère les enregistrements des catégories d'articles,
          des articles, des auteurs, et des sujets du forum depuis la base de données pour les afficher dans le back-end.
        - Si l'administrateur n'est pas encore authentifié, il est redirigé vers la page de connexion admin_connection.

    Example:
        L'administrateur accède à la route '/back_end' après s'être authentifié avec succès.
        Il peut visualiser et gérer les enregistrements des catégories d'articles, les articles eux-mêmes,
        les auteurs, et les sujets du forum.
    """
    # Vérifie si l'utilisateur est connecté en tant qu'administrateur.
    if "logged_in" in session and session["logged_in"]:
        # L'utilisateur est connecté en tant qu'administrateur, donc affiche le back-end.
        formcategories = NewCategorieForm()
        formarticles = ArticleForm()
        formsubjectforum = NewSubjectForumForm()
        formauthor = NewAuthor()
        formcomment = CommentForm()

        # Permet l'affichage des catégories, des articles de la liste des auteurs ainsi que les sujets du forum dans le back_end.
        categories = Categorie.query.all()
        articles = Article.query.all()
        authors = Author.query.all()
        pseudos = [author.pseudo for author in authors]
        subjects = SubjectForum.query.all()
        comments = Comment.query.all()

        return render_template("Admin/back_end.html", categories=categories, articles=articles, authors=authors,
                               pseudos=pseudos, subjects=subjects, comments=comments,
                               formcategories=formcategories, formarticles=formarticles,
                               formsubjectforum=formsubjectforum, formauthor=formauthor,
                               formcomment=formcomment)
    else:
        # L'utilisateur n'est pas connecté en tant qu'administrateur, redirige vers la page de connexion admin.
        return redirect(url_for("admin_connection"))


@app.route("/back_end_blog/articles")
def articles_list():
    """
    Affiche la liste de tous les articles, par titre, pseudo d'auteur, date et nombre de commentaires.

    Returns :
        La liste de tous les articles.
    """
    # Récupération de tous les articles depuis la base de données.
    articles = Article.query.all()

    return render_template("Admin/articles_list.html", articles=articles)


# route permettant de créer une nouvelle catégorie.
@app.route("/back_end_blog/nouvelle_categorie", methods=["POST"])
def add_new_categorie():
    """
    Permet de créer une nouvelle catégorie d'articles.

    Returns :
        Redirige vers le back_end.
    """
    if request.method == "POST":
        # Saisie du nom de la catégorie.
        nom_categorie = escape(request.form.get("nom"))
        categorie = Categorie(nom=nom_categorie)

        # Enregistrement dans la base de données.
        db.session.add(categorie)
        db.session.commit()

        flash("La catégorie a bien été ajoutée" + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))
    return redirect(url_for("back_end"))


# Route permettant de supprimer d'une catégorie.
@app.route("/back_end_blog/supprimer_catégorie/<int:id>", methods=["POST"])
def suppress_categorie(id):
    """
    Supprime une catégorie.

    Args :
        id: L'identifiant de la catégorie à supprimer.

    Returns :
        Redirige vers le back_end après la suppression de la catégorie.
    """
    categorie = Categorie.query.get(id)
    if categorie:
        # Suppression de la categorie.
        db.session.delete(categorie)
        # Validation de l'action.
        db.session.commit()
        flash("La catégorie a été supprimée avec succès." + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))

        return redirect(url_for("back_end"))


# Route permettant d'ajouter un nouvel auteur d'article.
@app.route("/back_end_blog/nouvel_auteur", methods=["GET", "POST"])
def add_new_author():
    """
    Créer un nouvel auteur.
    :return:
    """
    if request.method == "POST":
        # Saisie des caractéristiques de l'auteur.
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        pseudo = request.form.get("pseudo")

        author = Author(nom=nom, prenom=prenom, pseudo=pseudo)

        # Enregistrement dans la base de données.
        db.session.add(author)
        db.session.commit()

        flash("L'auteur a bien été ajouté " + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))
        return redirect(url_for("back_end"))


# Route pour supprimer un auteur.
@app.route("/back_end_blog/supprimer_auteur/<int:id>", methods=["POST"])
def suppress_author(id):
    """
    Supprime un auteur.

    Args :
        id: L'identifiant de l'auteur à supprimer.

    Returns :
        Redirige vers le back_end après la suppression de l'auteur.
    """
    author = Author.query.get(id)
    if author:
        # Suppression de l'auteur.
        db.session.delete(author)
        # validation de la suppression.
        db.session.commit()

        flash("L'auteur a bien été supprimé " + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))
        return redirect(url_for("back_end"))


# Route permettant de créer de noubeaux articles.
@app.route("/back_end_blog/nouvel_article", methods=["GET", "POST"])
def add_new_article():
    """
    Crée un nouvel article.

    Returns :
        Redirige vers le back_end après la création de l'article.
    """
    if request.method == "POST":
        # Saisie des caractéristiques de l'article.
        title = request.form.get("title")
        resume = request.form.get('resume')
        article_content = request.form.get("article_content")
        date_edition = request.form.get("date_edition")
        author_id = request.form.get('author_id')
        author = Author.query.filter_by(id=author_id).first()
        categorie_id = request.form.get("categorie_id")
        categorie = Categorie.query.filter_by(id=categorie_id).first()

        article = Article(title=title, resume=resume, article_content=article_content, date_edition=date_edition,
                          author=author, categorie=categorie)

        # Enregistrement de l'article dans la base de données.
        db.session.add(article)
        db.session.commit()

    flash("L'article a bien été ajouté " + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))
    return redirect(url_for("back_end"))


# Route permettant de supprimer un article du blog.
@app.route("/back_end_blog/supprimer_article/<int:id>", methods=["POST"])
def suppress_article(id):
    """
    Supprime un article.

    Returns :
        Redirige vers le back_end après la suppression de l'article.
    """
    article = Article.query.get(id)
    if article:
        # Suppression de l'article.
        db.session.delete(article)
        # Validation de l'action.
        db.session.commit()
        flash("L'article a été supprimé avec succès." + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))

    return redirect(url_for("back_end"))


@app.route("/back_end_blog/ajouter_sujet", methods=['POST'])
def add_subject_forum_back():
    """
    Permet de créer un nouveau sujet pour le forum à partir du back_end.

    Returns :
        Redirige vers la page du back_end.
    """
    if request.method == "POST":
        # Saisie du nom du sujet.
        nom_subject_forum = escape(request.form.get("nom"))
        subject_forum = SubjectForum(nom=nom_subject_forum)

        # Enregistrement du sujet dans la base de données.
        db.session.add(subject_forum)
        db.session.commit()

    return redirect(url_for("back_end"))


# Route permettant de supprimer un sujet du forum.
@app.route("/back_end_blog/supprimer_sujet/<int:id>", methods=["POST"])
def suppress_subject(id):
    """
    Supprime un sujet du forum.

    Returns :
        Redirige vers le back_end après la suppression du sujet.
    """
    subject = SubjectForum.query.get(id)
    if subject:
        # Suppression du sujet.
        db.session.delete(subject)
        # Validation de l'action.
        db.session.commit()
        flash("Le sujet a été supprimé avec succès." + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))

    return redirect(url_for("back_end"))


@app.route("/back_end_blog/supprimer_commentaires/<int:id>", methods=['GET', 'POST'])
def suppress_comment(id):
    """
    Route pour supprimer un commentaire du blog.

    Args:
        id (int): L'identifiant du commentaire à supprimer.

    Returns:
        Redirige vers la page d'administration après la suppression.

    """

    comment = Comment.query.get(id)
    if comment:
        # Suppression du sujet.
        db.session.delete(comment)
        # Validation de l'action.
        db.session.commit()
        flash("Le commentaire a été supprimé avec succès." + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))

    return redirect(url_for("back_end"))


@app.route("/enregistrement_membre", methods=['GET', 'POST'])
def user_recording():
    """
     Enregistrement du membre dans la base de données du site.
     """
    form = UserSaving()
    if form.validate_on_submit():
        pseudo = form.pseudo.data
        password_hash = form.password.data
        email = form.email.data
        date_naissance = form.date_naissance.data

        # Création du sel et hachage du mot de passe
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_hash.encode('utf-8'), salt)

        # Enregistrement dans la table "User".
        user = User(pseudo=pseudo, password_hash=password_hash, salt=salt, email=email,
                    date_naissance=date_naissance)
        db.session.add(user)
        db.session.commit()

        flash("Inscription réussie! Vous pouvez maintenant vous connecter.")
        return redirect(url_for("landing_page"))

    return render_template("User/form_user.html", form=form)


@app.route("/connexion_utilisateur_formulaire", methods=['GET', 'POST'])
def user_connection():
    """
    Permet à l'utilisateur d'accéder au formulaire de connexion afin de s'identifier.

    Return :
        Redirige vers le formulaire d'authentification utilisateur.
    """
    next_url = request.referrer
    print(next_url)
    session['next_url'] = next_url
    form = UserConnection()
    return render_template("User/user_connection.html", form=form, next_url=next_url)


@app.route("/connexion_utilisateur", methods=['GET', 'POST'])
def login():
    """
    Gère l'authentification de l'utilisateur afin qu'il puisse laisser un commentaire ou
    ajouter un sujet sur le forum.
    Returns:
        Redirige l'utilisateur sur la page d'accueil avec son nom sur le fichier html.
    """
    # Récupère next_url depuis la session Flask
    next_url = session.get('next_url')
    print(next_url)

    # Création de l'instance du formulaire.
    form = UserConnection()

    if request.method == 'POST':
        if form.validate_on_submit():
            pseudo = form.pseudo.data
            password = form.password.data

            # Validation de la connexion.
            user = User.query.filter_by(pseudo=pseudo).first()
            login_user(user)
            if user is not None and bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
                # Authentification réussie
                app.logger.info(f"L'utilisateur {user.pseudo} s'est bien connecté.")
                # Connexion de l'utilisateur et stockage de ses informations dans la session.
                session["logged_in"] = True
                session["pseudo"] = user.pseudo
                session["user_id"] = user.id

            if next_url:
                return redirect(next_url)
            else:
                return redirect(url_for('landing_page'))

        else:
            app.logger.warning(
                f"Tentative de connexion échouée avec l'utilisateur {form.pseudo.data}.")
            return redirect(url_for("user_connection"))


# Fonction de vérification de l'état de connexion
def check_logged_in():
    """
    Vérifie si l'utilisateur est connecté.
    Si l'utilisateur n'est pas connecté, redirige vers la page de connexion.
    """
    if not session.get("logged_in"):
        return redirect(url_for("user_connection"))


@app.route("/forum", methods=['GET', 'POST'])
def forum():
    """"
    Page du forum.

    Returns :
        La page du forum.
    """
    # Création de l'instance du formulaire.
    formsubjectforum = NewSubjectForumForm()

    # Récupération de tous les sujets de la table de données.
    subjects = SubjectForum.query.all()

    return render_template("Presentation/forum.html", formsubjectforum=formsubjectforum, subjects=subjects)


@app.route("/forum/ajouter_sujet", methods=['POST'])
@login_required
def add_subject_forum():
    """
    Permet de créer un nouveau sujet pour le forum.

    Returns :
        Redirige vers la page du forum.
    """
    # Vérifie l'état de connexion de l'utilisateur
    check_logged_in()

    # Création de l'instance du formulaire.
    formsubjectforum = NewSubjectForumForm()
    if request.method == "POST":
        # Saisie du nom du sujet.
        nom_subject_forum = escape(request.form.get("nom"))
        subject_forum = SubjectForum(nom=nom_subject_forum)

        # Enregistrement du sujet dans la base de données.
        db.session.add(subject_forum)
        db.session.commit()

    # Récupérer à nouveau tous les sujets après l'ajout du nouveau sujet
    subjects = SubjectForum.query.all()

    return render_template("Presentation/forum.html", formsubjectforum=formsubjectforum, subjects=subjects) + '#sujet'


@app.route("/<string:user_pseudo>/commentaires", methods=['POST'])
@login_required
def comment_article(user_pseudo):
    """
    Permet à uin utilisateur de laisser un commentaire sur un article.

    Args:
        user_pseudo(str): le pseudo de l'utilisateur.

    Returns:
         Redirige vers al page de l'article après avoir laissé un commentaire.
    """
    # Création de l'instance du formulaire.
    formcomment = CommentForm()

    if request.method == 'POST':
        # Obtention de l'id de l'article à partir de la requête POST.
        article_id = request.form.get("article_id")

        # Obtention de l'utilisateur actuel à partir du pseudo.
        user = User.query.filter_by(pseudo=user_pseudo).first()

        # Vérification de l'existence de l'utilisateur et de l'article.
        if user and article_id:
            # Obtenir le contenu du commentaire à partir de la requête POST.
            comment_content = request.form.get("comment_content")
            # Capture de la date actuelle.
            date = datetime.now().date()

            # Créer un nouvel objet de commentaire.
            new_comment = Comment(comment_content=comment_content, user_id=user.id, article_id=article_id)

            # Ajouter le nouveau commentaire à la table de données.
            db.session.add(new_comment)
            db.session.commit()

            # Récupération de tous les commentaires de l'article après ajout du commentaire.
            comment_content = Comment.query.filter_by(article_id=article_id).first()

            # Redirection sur la page d'affichage des articles.
            return redirect(url_for("show_article", article_id=article_id, comment_content=comment_content))
        else:
            # Redirection vers une autre page si l'utilisateur n'existe pas.
            return redirect(url_for("connection_requise"))


@app.route("/like_comment/<int:comment_id>", methods=['POST'])
def comment_like(comment_id):
    """

    :param comment_id:
    :return:
    """
    # Récupération des commentaires.
    comment = Comment.query.get_or_404(comment_id)
    # Ajout d'un like.
    comment.likes += 1
    # Enregistrement dans la base de données.
    db.session.commit()

    return redirect(url_for('show_article'))


@app.route("/dislike_comment/<int:comment_id>", methods=['POST'])
def comment_dislike(comment_id):
    """

    :param comment_id:
    :return:
    """
    # Récupération des commentaires.
    comment = Comment.query.get_or_404(comment_id)
    # Ajout d'un dislike.
    comment.dislikes += 1
    # Enregistrement dans la base de données.
    db.session.commit()

    return redirect(url_for('show_article'))


@app.route("/<string:user_pseudo>/comment<int:comment_id>/reply_form", methods=['GET'])
@login_required
def reply_form(comment_id, user_pseudo):
    """
    Affiche le formulaire pour répondre à un commentaire.
    """

    # Création d'une instance du formulaire.
    formreply = ReplyForm()

    comment = db.session.get(Comment, comment_id)

    user = User.query.filter_by(pseudo=user_pseudo).first()

    return render_template("User/reply_form.html", form=formreply, comment=comment, user=user)


@app.route("/<string:user_pseudo>/comment<int:comment_id>/reply", methods=['GET', 'POST'])
@login_required
def comment_replies(comment_id, user_pseudo):
    """
    Permet à un utilisateur de laisser une réponse à un commentaire.

    Args:
        comment_id(int): l'identifiant du commentaire.
        user_pseudo(str): le pseudo de l'utilisateur.

    Returns:
         Redirige vers la page de l'article après avoir laissé une réponse.
    """
    # Création de l'instance du formulaire.
    formreply = ReplyForm()

    # Récupérer le commentaire par son id.
    comment = db.session.get(Comment, comment_id)
    # Récupération de l'ID de l'article du commentaire.
    article_id = comment.article_id

    if request.method == 'POST':

        if formreply.validate_on_submit():
            # Obtention de l'utilisateur actuel à partir du pseudo.
            user = User.query.filter_by(pseudo=user_pseudo).first()

            # Vérification de l'existence de l'utilisateur et du commentaire.
            if user and comment:
                # Obtenir le contenu du commentaire à partir de la requête POST.
                reply_content = formreply.reply_content.data

                # Créer un nouvel objet de commentaire.
                new_reply = Reply(reply_content=reply_content, user_id=user.id, comment_id=comment_id)

                # Ajouter le nouveau commentaire à la table de données.
                db.session.add(new_reply)
                db.session.commit()
                print('la réponse au commentaire à bien été enregistrée.')

                # Redirection sur la page d'affichage des articles.
                return redirect(url_for("show_article", article_id=article_id))
            else:
                # Redirection vers une autre page si l'utilisateur n'existe pas.
                return redirect(url_for("connection_requise"))

    return redirect(url_for('show_article', article_id=article_id))


@app.route("/Politique_de_confidentialité")
def politique():
    """
    Accès à la Politique de confidentialité du blog.

    Returns :
        Redirige vers la page de politique de confidentialité du blog.
    """
    return render_template("Fonctional/politique.html")


@app.route("/mentions_légales")
def mentions():
    """
    Accès aux Mentions légales du blog.
    Returns :
        Redirige vers la page de politique de confidentialité du blog.
    """
    return render_template("Fonctional/mentions.html")


if __name__ == '__main__':
    app.run(debug=True)
