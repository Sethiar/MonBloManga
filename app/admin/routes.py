"""
Code permettant de définir les routes concernant l'administration du blog.
"""

from app.admin import admin_bp

from datetime import datetime
from flask import flash, redirect, url_for, session, render_template,\
    request
from markupsafe import escape

from Models import db
from Models.comment_article import CommentArticle

from Models.forms import ArticleForm, NewCategorieForm, NewAuthor, NewSubjectForumForm, UserSaving, \
    CommentArticleForm, CommentSubjectForm, FilterForm, SuppressCommentSubjectForm, CreateMangakaForm
from Models.categories_articles import Categorie
from Models.author import Author
from Models.articles import Article
from Models.mangaka import BiographyMangaka
from Models.comment_subject import CommentSubject
from Models.user import User
from Models.subjects_forum import SubjectForum


# Route utilisée pour accéder au back_end du blog.
@admin_bp.route("/back_end")
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
        formcomment = CommentArticleForm()
        formuser = UserSaving()

        # Permet l'affichage des catégories, des articles de la liste des auteurs ainsi que les sujets du forum dans
        # le back_end.
        categories = Categorie.query.all()
        articles = Article.query.all()
        authors = Author.query.all()
        users = User.query.all()
        pseudos = [author.pseudo for author in authors]
        subjects = SubjectForum.query.all()
        comments = CommentArticle.query.all()

        return render_template("Admin/back_end.html", categories=categories,
                               articles=articles, authors=authors, pseudos=pseudos, subjects=subjects,
                               comments=comments, users=users,
                               formcategories=formcategories, formarticles=formarticles,
                               formsubjectforum=formsubjectforum, formauthor=formauthor,
                               formcomment=formcomment, formuser=formuser)
    else:
        # L'utilisateur n'est pas connecté en tant qu'administrateur, redirige vers la page de connexion admin.
        return redirect(url_for("auth.admin_connection"))


@admin_bp.route("/back_end_blog/articles")
def articles_list():
    """
    Affiche la liste de tous les articles, par titre, pseudo d'auteur, date et nombre de commentaires.

    Returns :
        La liste de tous les articles.
    """
    formarticles = ArticleForm()
    formfiltercategorie = FilterForm()

    # Récupération de toutes les catégories depuis les articles
    categories = Categorie.query.all()
    formfiltercategorie.category.choices = [(cat.nom, cat.nom) for cat in categories]

    # Récupération de tous les articles.
    articles = Article.query.all()

    return render_template("Admin/articles_list.html", articles=articles,
                           formarticles=formarticles, formfiltercategorie=formfiltercategorie,
                           categories=categories)


@admin_bp.route("/back_end_blog/articles/by_category", methods=['GET', 'POST'])
def article_filter():
    """
    Affiche la liste des articles en les filtrant par catégorie.

    Returns:
        La liste des articles filtrés par catégorie.
    """
    formfiltercategorie = FilterForm()

    # Peuplez les choix pour le champ category
    formfiltercategorie.category.choices = [(cat.nom, cat.nom) for cat in Categorie.query.all()]

    # Par défaut, récupérer tous les articles
    articles = Article.query.all()

    if formfiltercategorie.validate_on_submit():
        category_name = request.form.get('category')
        print(f"Nom de la catégorie reçu du formulaire : {category_name}")

        if category_name:
            # Récupération de l'id de la catégorie sélectionnée.
            category = Categorie.query.filter_by(nom=category_name).first()
            print(f"Catégorie récupérée : {category}")

            if category:
                # Filtrage des articles par l'id de la catégorie.
                articles = Article.query.filter_by(categorie_id=category.id).all()
                print(f"Articles filtrés par catégorie (id={category.id}) : {articles}")
            else:
                articles = []
                print("Aucune catégorie trouvée avec ce nom.")
        else:
            print("Aucune catégorie spécifiée, récupération de tous les articles.")
    else:
        # Afficher les erreurs de validation
        print("Formulaire non validé. Erreurs :")
        print(formfiltercategorie.errors)

    # Assurez-vous que la sélection reste après la soumission
    if request.method == 'POST':
        formfiltercategorie.category.data = request.form.get('category')

    return render_template("Admin/articles_list.html", articles=articles,
                           formarticles=ArticleForm(), formfiltercategorie=formfiltercategorie)


@admin_bp.route("/back_end_blog/liste_utilisateur")
def users_list():
    """
    Route permettant d'accéder à la liste des utilisateurs enregistrés sur le blog.
    :return:
    """
    formuser = UserSaving()
    users = db.session.query(User.id, User.pseudo, User.email).all()

    user_data = [
        {'id': user_id, 'pseudo': pseudo, 'email': email}
        for user_id, pseudo, email in users
    ]

    return render_template("Admin/users_list.html", users=user_data, formuser=formuser)


# Route permettant de supprimer d'un utilisateur.
@admin_bp.route("/back_end_blog/supprimer_utilisateur/<int:id>", methods=["POST"])
def suppress_user(id):
    """
    Supprime un utilisateur.

    Args :
        id: L'identifiant de l'utilisateur à supprimer.

    Returns :
        Redirige vers le back_end après la suppression de l'utilisateur.
    """
    user = User.query.get(id)
    if user:
        # Suppression de l'utilisateur.
        db.session.delete(user)
        # Validation de l'action.
        db.session.commit()
        flash("L'utilisateur a été supprimé avec succès." + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))

        return redirect(url_for("admin.users_list"))


@admin_bp.route("/back_end_blog/bannir_utilisateur/<int:id>", methods=['GET', 'POST'])
def banned_user(id):
    """
    Route pour bannir un utilisateur.

    Args:
        id (int):L'identifiant de l'utilisateur à bannir.

    Returns:
        Redirige vers la page de bannissement après l'action.
    :param id:
    :return:
    """
    pass


# route permettant de créer une nouvelle catégorie.
@admin_bp.route("/back_end_blog/nouvelle_categorie", methods=["POST"])
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
    return redirect(url_for("admin.back_end"))


# Route permettant de supprimer d'une catégorie.
@admin_bp.route("/back_end_blog/supprimer_catégorie/<int:id>", methods=["POST"])
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

        return redirect(url_for("admin.back_end"))


# Route permettant d'ajouter un nouvel auteur d'article.
@admin_bp.route("/back_end_blog/nouvel_auteur", methods=["GET", "POST"])
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
        return redirect(url_for("admin.back_end"))


# Route pour supprimer un auteur.
@admin_bp.route("/back_end_blog/supprimer_auteur/<int:id>", methods=["POST"])
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
        return redirect(url_for("admin.back_end"))


# Route permettant de créer de noubeaux articles.
@admin_bp.route("/back_end_blog/nouvel_article", methods=["GET", "POST"])
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
    return redirect(url_for("admin.back_end"))


# Route permettant de supprimer un article du blog.
@admin_bp.route("/back_end_blog/supprimer_article/<int:id>", methods=["POST"])
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

    return redirect(url_for("admin.back_end"))


@admin_bp.route("/back_end_blog/commentaires_article_utilisateurs", methods=['GET', 'POST'])
def users_comments():
    """
    Route permettant de voir chaque commentaire en fonction de l'utilisateur.
    """
    formuser = UserSaving()
    user_comments = {}

    comments = CommentArticle.query.all()
    for comment in comments:
        user = User.query.get(comment.user_id)
        article = Article.query.get(comment.article_id)
        if user.pseudo not in user_comments:
            user_comments[user.pseudo] = []
        user_comments[user.pseudo].append({
            'article': article,
            'comment': comment
        })

    return render_template("admin/users_comments.html", user_comments=user_comments, formuser=formuser)


@admin_bp.route("back_end_blog/filtrage_utilisateur_article_alphabet", methods=['GET', 'POST'])
def users_articles_alpha_filter():
    """
    Route permettant de filtrer les utilisateurs par la première lettre de leur pseudo.
    """
    formuser = ArticleForm()

    lettre = request.args.get('lettre', type=str)
    if lettre:
        users = User.query.filter(User.pseudo.ilike(f'{lettre}%')).order_by(
            User.pseudo.asc()).all()
    else:
        users = User.query.order_by(User.pseudo.asc()).all()

    user_comments = {}
    for user in users:
        comments = CommentArticle.query.filter_by(user_id=user.id).all()
        for comment in comments:
            article = Article.query.get(comment.article_id)
            if user.pseudo not in user_comments:
                user_comments[user.pseudo] = []
            user_comments[user.pseudo].append({
                'article': article,
                'comment': comment
            })
    return render_template('admin/users_comments.html', user_comments=user_comments, formuser=formuser)


@admin_bp.route("/back_end_blog/supprimer_commentaires/<int:id>", methods=['GET', 'POST'])
def suppress_comment_article(id):
    """
    Route pour supprimer un commentaire du blog.

    Args:
        id (int): L'identifiant du commentaire à supprimer.

    Returns:
        Redirige vers la page de visualisation des commentaires en fonction des utilisateurs après la suppression.

    """

    comment = CommentArticle.query.get(id)
    if comment:
        # Suppression du commentaire de l'article.
        db.session.delete(comment)
        # Validation de l'action.
        db.session.commit()
        flash("Le commentaire a été supprimé avec succès." + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))

    return redirect(url_for("admin.users_articles_alpha_filter"))


@admin_bp.route("/back_end_blog/ajouter_sujet", methods=['POST'])
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

    return redirect(url_for("admin.back_end"))


# Route permettant de supprimer un sujet du forum.
@admin_bp.route("/back_end_blog/supprimer_sujet/<int:id>", methods=["POST"])
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

    return redirect(url_for("admin.back_end"))


@admin_bp.route("/back_end_blog/commentaires_sujets_utilisateurs", methods=['GET', 'POST'])
def users_comments_subject():
    """
    Route permettant de voir chaque commentaire en fonction de l'utilisateur.
    """
    formuser = UserSaving()
    suppressform = SuppressCommentSubjectForm()
    user_comments = {}

    comments = CommentSubject.query.all()
    for comment in comments:
        user = User.query.get(comment.user_id)
        subject = SubjectForum.query.get(comment.subject_id)
        if user.pseudo not in user_comments:
            user_comments[user.pseudo] = []
        user_comments[user.pseudo].append({
            'sujet': subject,
            'comment': comment
        })

    return render_template("admin/users_subject_comments.html", user_comments=user_comments, formuser=formuser,
                           suppressform=suppressform)


@admin_bp.route("back_end_blog/filtrage_utilisateur_sujets_alphabet", methods=['GET', 'POST'])
def users_subject_alpha_filter():
    """
    Route permettant de filtrer les utilisateurs par la première lettre de leur pseudo.
    """
    formuser = CommentSubjectForm()
    suppressform = SuppressCommentSubjectForm()

    lettre = request.args.get('lettre', type=str)
    if lettre:
        users = User.query.filter(User.pseudo.ilike(f'{lettre}%')).order_by(
            User.pseudo.asc()).all()
    else:
        users = User.query.order_by(User.pseudo.asc()).all()

    user_comments = {}
    for user in users:
        comments = CommentSubject.query.filter_by(user_id=user.id).all()
        for comment in comments:
            subject = SubjectForum.query.get(comment.subject_id)
            if user.pseudo not in user_comments:
                user_comments[user.pseudo] = []
            user_comments[user.pseudo].append({
                'sujet': subject,
                'comment': comment
            })
    return render_template('admin/users_subject_comments.html', user_comments=user_comments, formuser=formuser,
                           suppressform=suppressform)


@admin_bp.route("/back_end_blog/supprimer_commentaires_sujets/<int:id>", methods=['GET', 'POST'])
def suppress_subject_comment(id):
    """
    Route pour supprimer un commentaire du blog.

    Args:
        id (int): L'identifiant du commentaire à supprimer.

    Returns:
        Redirige vers la page d'administration après la suppression.

    """
    comment = CommentSubject.query.get(id)
    if comment:
        # Suppression du sujet.
        db.session.delete(comment)
        # Validation de l'action.
        db.session.commit()
        flash("Le commentaire du blog a été supprimé avec succès." + " "
              + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))

    return redirect(url_for("admin.users_subject_alpha_filter"))


@admin_bp.route("/back_end_blog/ajout_mangaka", methods=['GET', 'POST'])
def create_mangaka():
    """
    Route permettant de créer une nouvelle biographie de mangaka.



    :return:
    """
    formmangaka = CreateMangakaForm()
    authors = Author.query.all()

    if request.method == "POST":
        # Saisie des caractéristiques de la biographie.
        mangaka_name = request.form.get("mangaka_name")
        biography_content = request.form.get("biography_content")
        date_bio_mangaka = request.form.get("date_bio_mangaka")
        author_id = request.form.get('author_id')
        author = Author.query.filter_by(id=author_id).first()

        biography_mangaka = BiographyMangaka(mangaka_name=mangaka_name, biography_content=biography_content,
                                             date_bio_mangaka=date_bio_mangaka, author=author)

        # Enregistrement de la biographie dans la base de données.
        db.session.add(biography_mangaka)
        db.session.commit()

    flash("La biographie a bien été ajoutée" + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))

    return render_template('Admin/create_mangaka.html', formmangaka=formmangaka, authors=authors)
