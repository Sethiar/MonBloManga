"""
Code permettant de définir les routes concernant l'administration du blog.
"""

from app.admin import admin_bp

from datetime import datetime
from flask import flash, redirect, url_for, session, render_template,\
    request

from markupsafe import escape

from app.Models import db

from app.Models.forms import ArticleForm, NewCategorieForm, NewAuthor, NewSubjectForumForm, UserSaving, \
    CommentArticleForm, CommentSubjectForm, CommentBiographyForm, FilterForm, SuppressCommentSubjectForm,\
    CreateMangakaForm, SuppressCommentBiographyForm, DeleteBiographyForm, BanUserForm, UnBanUserForm

from app.Models.categories_articles import Categorie
from app.Models.author import Author
from app.Models.articles import Article
from app.Models.user import User

from app.Models.comment_article import CommentArticle
from app.Models.biographies import BiographyMangaka
from app.Models.comment_biography import CommentBiography
from app.Models.comment_subject import CommentSubject
from app.Models.subjects_forum import SubjectForum

from app.mail.routes import mail_banned_user, mail_deban_user, mail_edit_article


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


# Route permettant d'accéder à la liste des articles.
@admin_bp.route("/back_end_blog/articles")
def articles_list():
    """
    Affiche la liste de tous les articles, par titre, pseudo d'auteur, date et nombre de commentaires.

    Returns :
        La liste de tous les articles avec des détails tels que le titre, le pseudo de l'auteur,
        la date d'édition et le nombre de commentaires associés à chaque article.
    """
    formarticles = ArticleForm()
    formfiltercategorie = FilterForm()

    # Récupération de toutes les catégories depuis les articles.
    categories = Categorie.query.all()
    formfiltercategorie.category.choices = [(cat.name, cat.name) for cat in categories]

    # Récupération de tous les articles.
    articles = Article.query.all()

    return render_template("Admin/articles_list.html", articles=articles,
                           formarticles=formarticles, formfiltercategorie=formfiltercategorie,
                           categories=categories)


# Route permettant de filtrer les articles par catégorie.
@admin_bp.route("/back_end_blog/articles/by_category", methods=['GET', 'POST'])
def article_filter():
    """
    Affiche la liste des articles en filtrant par catégorie.

    Cette route permet à l'administrateur de filtrer les articles en fonction de la catégorie sélectionnée.
    Les catégories sont récupérées depuis la base de données et affichées dans un formulaire dédié.

    Returns:
        template: Une vue contenant la liste des articles filtrés par catégorie, avec la possibilité de
        sélectionner une catégorie spécifique.
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
            category = Categorie.query.filter_by(name=category_name).first()
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


# Route permettant de visualiser la liste des utilisateurs.
@admin_bp.route("/back_end_blog/liste_utilisateur")
def users_list():
    """
    Affiche la liste des utilisateurs enregistrés sur le blog.

    Cette route permet à l'administrateur de voir tous les utilisateurs enregistrés,
    avec leurs détails tels que pseudo, email et statut de bannissement.

    Returns:
        template: Une vue contenant la liste des utilisateurs avec des options pour les actions
        telles que sauvegarder, bannir ou débannir un utilisateur.
    """
    # Instanciation des formulaires.
    formuser = UserSaving()
    formban = BanUserForm()
    formunban = UnBanUserForm()

    users = db.session.query(User.id, User.pseudo, User.email, User.banned, User.count_ban).all()

    user_data = [
        {'id': user_id, 'pseudo': pseudo, 'email': email, 'banned': banned, 'count_ban': count_ban}
        for user_id, pseudo, email, banned, count_ban in users
    ]

    return render_template("Admin/users_list.html", users=user_data, formuser=formuser,
                           formban=formban, formunban=formunban)


# Route permettant de supprimer d'un utilisateur.
@admin_bp.route("/back_end_blog/supprimer_utilisateur/<int:id>", methods=["POST"])
def suppress_user(id):
    """
    Supprime un utilisateur du système.

    Cette route permet à l'administrateur de supprimer définitivement un utilisateur du système,
    identifié par son ID. Après la suppression, l'utilisateur est complètement retiré de la base de données.

    Args:
        id (int): L'identifiant unique de l'utilisateur à supprimer.

    Returns:
        Response: Redirection vers la page de liste des utilisateurs après la suppression.

    """
    user = User.query.get(id)
    if user:
        # Suppression de l'utilisateur.
        db.session.delete(user)
        # Validation de l'action.
        db.session.commit()
        flash("L'utilisateur a été supprimé avec succès." + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))

        return redirect(url_for("admin.users_list"))


# Route permettant de bannir un utilisateur.
@admin_bp.route("/back_end_blog/bannir_utilisateur/<int:id>", methods=['GET', 'POST'])
def banning_user(id):
    """
    Bannit un utilisateur.

    Cette route permet à l'administrateur de bannir un utilisateur spécifique, identifié par son ID,
    en utilisant un formulaire POST. L'utilisateur est banni en appelant la méthode `ban_user()`
    sur l'objet `User`. Après le bannissement, l'utilisateur est redirigé vers la page de gestion des utilisateurs.

    Args:
        id (int): L'identifiant unique de l'utilisateur à bannir.

    Returns:
        Response: Redirection vers la page de gestion des utilisateurs après le bannissement.

    """
    # Instanciation du formulaire de bannissement.
    formban = BanUserForm()
    # Récupération de l'utilisateur à bannir par son identifiant.
    user = User.query.get(id)

    if user:
        # Bannissement de l'utilisateur.
        user.ban_user()
        # Récupération de l'email de l'utilisateur.
        email = user.email
        mail_banned_user(email)

        flash("l'utilisateur est banni du blog.")
    else:
        flash("L'utilisateur n'a pas été trouvé.", "error")

    return redirect(url_for('admin.back_end', formban=formban))


# Route permettant de bannir un utilisateur.
@admin_bp.route("/back_end_blog/débannir_utilisateur/<int:id>", methods=['GET', 'POST'])
def unbanning_user(id):
    """
    Débannit un utilisateur.

    Cette route permet à l'administrateur de débannir un utilisateur spécifique, identifié par son ID,
    en utilisant un formulaire POST. L'utilisateur est débanni en appelant la méthode `unban_user()`
    sur l'objet `User`. Après le débannissement, l'utilisateur est redirigé vers la page de gestion des utilisateurs.

    Args:
        id (int): L'identifiant unique de l'utilisateur à débannir.

    Returns:
        Response: Redirection vers la page de gestion des utilisateurs après le débannissement.

    """
    # Instanciation du formulaire de débannissement.
    formban = BanUserForm()
    formunban = UnBanUserForm()

    # Récupération de l'utilisateur à débannir par son identifiant.
    user = User.query.get(id)

    if user:
        # Débannissement de l'utilisateur.
        user.unban_user()
        # Récupération de l'email de l'utilisateur.
        email = user.email
        mail_deban_user(email)

        flash("l'utilisateur est réintégré au blog.")
    else:
        flash("L'utilisateur n'a pas été trouvé.", "error")

    return redirect(url_for('admin.back_end', formban=formban, formunban=formunban))


# Route permettant de créer une nouvelle catégorie.
@admin_bp.route("/back_end_blog/nouvelle_categorie", methods=["POST"])
def add_new_categorie():
    """
    Crée une nouvelle catégorie d'articles pour le blog.

    Cette route permet à l'administrateur de créer une nouvelle catégorie pour les articles en utilisant
    un formulaire POST. Le nom de la catégorie est saisi à partir du formulaire, enregistré dans la base
    de données, et l'administrateur est redirigé vers la page du back-end après la création de la catégorie.

    Returns:
        Response: Redirection vers la page du back-end après la création de la catégorie.

    """
    if request.method == "POST":
        # Saisie du nom de la catégorie.
        name_categorie = escape(request.form.get("name"))
        categorie = Categorie(name=name_categorie)

        # Enregistrement dans la base de données.
        db.session.add(categorie)
        db.session.commit()

        flash("La catégorie a bien été ajoutée" + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))
    return redirect(url_for("admin.back_end"))


# Route permettant de supprimer d'une catégorie.
@admin_bp.route("/back_end_blog/supprimer_catégorie/<int:id>", methods=["POST"])
def suppress_categorie(id):
    """
    Supprime une catégorie de la base de données.

    Cette route permet à l'administrateur de supprimer une catégorie spécifique, identifiée par son ID,
    de la base de données. Après la suppression, un message de confirmation est affiché et
    l'administrateur est redirigé vers la page du back-end.

    Args:
        id (int): L'identifiant unique de la catégorie à supprimer.

    Returns:
        Response: Une redirection vers la page du back-end après la suppression de la catégorie.

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
    Crée un nouvel auteur pour les articles.

    Cette route permet à l'administrateur d'ajouter un nouvel auteur pour les articles en utilisant
    un formulaire POST. Les caractéristiques de l'auteur telles que le nom, le prénom et le pseudo
    sont saisies à partir du formulaire, enregistrées dans la base de données, et l'utilisateur est
    redirigé vers la page du back-end après l'ajout de l'auteur.

    Returns:
        Response: Redirection vers la page du back-end après l'ajout de l'auteur.

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
    Supprime un auteur de la base de données.

    Cette route permet à l'administrateur de supprimer un auteur spécifique, identifié par son ID,
    de la base de données. Après la suppression, un message de confirmation est affiché et
    l'administrateur est redirigé vers la page du back-end.

    Args:
        id (int): L'identifiant unique de l'auteur à supprimer.

    Returns:
        Response: Une redirection vers la page du back-end après la suppression de l'auteur.

    """
    author = Author.query.get(id)
    if author:
        # Suppression de l'auteur.
        db.session.delete(author)
        # validation de la suppression.
        db.session.commit()

        flash("L'auteur a bien été supprimé " + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))
        return redirect(url_for("admin.back_end"))


# Route permettant de créer de nouveaux articles.
@admin_bp.route("/back_end_blog/nouvel_article", methods=["GET", "POST"])
def add_new_article():
    """
    Crée un nouvel article pour le blog.

    Cette route permet à l'administrateur de créer un nouvel article pour le blog en utilisant
    un formulaire POST. Les caractéristiques de l'article telles que le titre, le résumé,
    le contenu, la date d'édition, l'auteur et la catégorie sont saisies à partir du formulaire,
    enregistrées dans la base de données, et l'utilisateur est redirigé vers la page du back-end
    après la création de l'article.

    Returns:
        Response: Redirection vers la page du back-end après la création de l'article.

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

        try:
            # Enregistrement de l'article dans la base de données.
            db.session.add(article)
            db.session.commit()

            # Envoi d'un mail pour la publication d'un article.
            users = User.query.all()
            for user in users:
                mail_edit_article(user.email, article)

            flash("L'article a bien été ajouté " + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de la création de l'article: {str(e)}")

        return redirect(url_for("admin.back_end"))

    return redirect(url_for("admin.back_end"))


# Route permettant de supprimer un article du blog.
@admin_bp.route("/back_end_blog/supprimer_article/<int:id>", methods=["POST"])
def suppress_article(id):
    """
    Supprime un article du blog.

    Cette route permet de supprimer un article spécifique, identifié par son ID,
    du blog. Après la suppression, un message de confirmation est affiché et
    l'utilisateur est redirigé vers la page du back-end.

    Args:
        id (int): L'identifiant unique de l'article à supprimer.

    Returns:
        Response: Une redirection vers la page du back-end après la suppression de l'article.

    """
    article = Article.query.get(id)
    if article:
        # Suppression de l'article.
        db.session.delete(article)
        # Validation de l'action.
        db.session.commit()
        flash("L'article a été supprimé avec succès." + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))

    return redirect(url_for("admin.back_end"))


# Route permettant de visualiser les commentaires des utilisateurs de la section article.
@admin_bp.route("/back_end_blog/commentaires_article_utilisateurs", methods=['GET', 'POST'])
def users_comments():
    """
    Filtre les utilisateurs par la première lettre de leur pseudo et affiche leurs commentaires sur les articles.

    Cette route permet de filtrer les utilisateurs en fonction de la première lettre de leur pseudo.
    Les utilisateurs filtrés et leurs commentaires sur les articles sont affichés dans une page HTML.

    Args:
        None

    Returns:
        Response: Une page HTML affichant les utilisateurs filtrés et leurs commentaires sur les articles.

    Templates:
        admin/users_comments.html: Le modèle utilisé pour rendre la page des commentaires des utilisateurs.

    Context:
        formuser (ArticleForm): Formulaire pour les articles.
        user_comments (dict): Dictionnaire contenant les utilisateurs et leurs commentaires sur les articles.
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


# Route permettant de rechercher les auteurs des commentaires par la première lettre de leur pseudo.
@admin_bp.route("back_end_blog/filtrage_utilisateur_article_alphabet", methods=['GET', 'POST'])
def users_articles_alpha_filter():
    """
    Route permettant de filtrer les utilisateurs par la première lettre de leur pseudo.
    """
    formuser = ArticleForm()
    formban = BanUserForm()

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
    return render_template('admin/users_comments.html', user_comments=user_comments, formuser=formuser, formban=formban)


# Route permettant de supprimer le commentaire d'un utilisateur selon l'article.
@admin_bp.route("/back_end_blog/supprimer_commentaires/<int:id>", methods=['GET', 'POST'])
def suppress_comment_article(id):
    """
    Supprime un commentaire d'un article du blog.

    Cette route permet de supprimer un commentaire spécifique, identifié par son ID,
    d'un article dans le blog. Après la suppression, un message de confirmation est affiché et
    l'utilisateur est redirigé vers la page de visualisation des commentaires par utilisateur.

    Args:
        id (int): L'identifiant unique du commentaire à supprimer.

    Returns:
        Response: Une redirection vers la page de visualisation des commentaires par utilisateur après la suppression.

    """
    comment = CommentArticle.query.get(id)
    if comment:
        # Suppression du commentaire de l'article.
        db.session.delete(comment)
        # Validation de l'action.
        db.session.commit()
        flash("Le commentaire a été supprimé avec succès." + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))

    return redirect(url_for("admin.users_articles_alpha_filter"))


# Route permettant à l'administrateur d'ajouter un sujet au forum.
@admin_bp.route("/back_end_blog/ajouter_sujet", methods=['POST'])
def add_subject_forum_back():
    """
    Permet à l'administrateur d'ajouter un nouveau sujet pour le forum à partir du back-end.

    Cette route permet à l'administrateur d'ajouter un nouveau sujet pour le forum en utilisant
    un formulaire POST. Le nom du sujet est extrait du formulaire, enregistré dans la base de données,
    et l'utilisateur est redirigé vers la page du back-end après l'ajout.

    Returns:
        Response: Redirection vers la page du back-end après l'ajout du sujet.

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

    Cette route permet de supprimer un sujet spécifique, identifié par son ID,
    du forum. Après la suppression, un message de confirmation est affiché et
    l'utilisateur est redirigé vers la page d'administration.

    Args:
        id (int): L'identifiant unique du sujet à supprimer.

    Returns:
        Response: Une redirection vers la page d'administration après la suppression.

    """
    subject = SubjectForum.query.get(id)
    if subject:
        # Suppression du sujet.
        db.session.delete(subject)
        # Validation de l'action.
        db.session.commit()
        flash("Le sujet a été supprimé avec succès." + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))

    return redirect(url_for("admin.back_end"))


# Route permettant de visualiser les commentaires des utilisateurs en fonction du sujet du forum.
@admin_bp.route("/back_end_blog/commentaires_sujets_utilisateurs", methods=['GET', 'POST'])
def users_comments_subject():
    """
    Visualiser les commentaires des utilisateurs en fonction des sujets du forum.

    Cette route permet de voir tous les commentaires des utilisateurs sur les sujets du forum.
    Les commentaires sont regroupés par utilisateur et affichés dans une page HTML.

    Args:
        None

    Returns:
        Response: Une page HTML affichant les commentaires des utilisateurs sur les sujets du forum.

    Templates:
        admin/users_subject_comments.html: Le modèle utilisé pour rendre la page des commentaires des utilisateurs.

    Context:
        formuser (UserSaving): Formulaire pour les utilisateurs.
        suppressform (SuppressCommentSubjectForm): Formulaire pour supprimer des commentaires de sujets.
        user_comments (dict): Dictionnaire contenant les utilisateurs et leurs commentaires sur les sujets du forum.
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


# Route permettant de filtrer les commentaires en fonction des utilisateurs dans la section des sujets du forum.
@admin_bp.route("back_end_blog/filtrage_utilisateur_sujets_alphabet", methods=['GET', 'POST'])
def users_subject_alpha_filter():
    """
    Filtre les utilisateurs par la première lettre de leur pseudo et affiche leurs commentaires sur les sujets du forum.

    Cette route permet de filtrer les utilisateurs en fonction de la première lettre de leur pseudo.
    Les utilisateurs filtrés et leurs commentaires sur les sujets du forum sont affichés dans une page HTML.

    Args:
        None

    Returns:
        Response: Une page HTML affichant les utilisateurs filtrés et leurs commentaires sur les sujets du forum.

    Templates:
        admin/users_subject_comments.html: Le modèle utilisé pour rendre la page des commentaires des utilisateurs.

    Context:
        formuser (CommentSubjectForm): Formulaire pour les commentaires sur les sujets.
        suppressform (SuppressCommentSubjectForm): Formulaire pour supprimer des commentaires de sujets.
        user_comments (dict): Dictionnaire contenant les utilisateurs et leurs commentaires sur les sujets du forum.
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


# Route permettant de supprimer un commentaire d'un sujet du forum.
@admin_bp.route("/back_end_blog/supprimer_commentaires_sujets/<int:id>", methods=['GET', 'POST'])
def suppress_subject_comment(id):
    """
    Supprime un commentaire d'un sujet du forum.

    Cette route permet de supprimer un commentaire spécifique, identifié par son ID,
    d'un sujet dans le forum. Après la suppression, un message de confirmation
    est affiché et l'utilisateur est redirigé vers la page d'administration.

    Args:
        id (int): L'identifiant unique du commentaire à supprimer.

    Returns:
        Response: Une redirection vers la page d'administration après la suppression.

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


# Route permettant de créer une biographie.
@admin_bp.route("/back_end_blog/ajout_mangaka", methods=['GET', 'POST'])
def create_mangaka():
    """
    Crée une nouvelle biographie de mangaka.

    Cette route permet de créer une nouvelle biographie pour un mangaka.
    Les utilisateurs peuvent remplir un formulaire avec les détails de la biographie,
    et celle-ci est ensuite enregistrée dans la base de données.

    Args:
        None

    Returns:
        Response: Une page HTML avec le formulaire pour créer une nouvelle biographie et
                  les listes d'auteurs et de biographies existantes.

    Templates:
        Admin/create_mangaka.html: Le modèle utilisé pour rendre la page de création de biographie.

    Context:
        formmangaka (CreateMangakaForm): Formulaire pour créer une biographie de mangaka.
        authors (list): Liste de tous les auteurs disponibles.
        biographies (list): Liste de toutes les biographies existantes.
        delete_form (DeleteBiographyForm): Formulaire pour supprimer une biographie.
    """
    formmangaka = CreateMangakaForm()
    authors = Author.query.all()
    biographies = BiographyMangaka.query.all()
    delete_form = DeleteBiographyForm()

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

    return render_template('Admin/create_mangaka.html', formmangaka=formmangaka, authors=authors,
                           biographies=biographies, delete_form=delete_form)


# Route permettant de visualiser les commentaires des utilisateurs de la section biography.
@admin_bp.route("/back_end_blog/commentaires_biography_utilisateurs", methods=['GET', 'POST'])
def users_comments_biography():
    """
    Visualiser les commentaires des utilisateurs de la section biographie.

    Cette route permet de voir tous les commentaires des utilisateurs sur les biographies.
    Les commentaires sont regroupés par utilisateur et affichés dans une page HTML.

    Args:
        None

    Returns:
        Response: Une page HTML affichant les commentaires des utilisateurs sur les biographies.

    Templates:
        admin/users_comments_biography.html: Le modèle utilisé pour rendre la page des commentaires des utilisateurs.

    Context:
        formbiography (CreateMangakaForm): Formulaire pour créer un mangaka.
        user_comments_biography (dict): Dictionnaire contenant les utilisateurs et leurs commentaires sur les biographies.
    """
    formbiography = CreateMangakaForm()
    user_comments_biography = {}

    comments = CommentBiography.query.all()
    for comment in comments:
        user = User.query.get(comment.user_id)
        biography = BiographyMangaka.query.get(comment.biography_mangaka_id)
        if user.pseudo not in user_comments_biography:
            user_comments_biography[user.pseudo] = []
        user_comments_biography[user.pseudo].append({
            'biography': biography,
            'comment': comment
        })

    return render_template("admin/users_comments_biography.html", user_comments_biography=user_comments_biography,
                           formbiography=formbiography)


# Route permettant de filtrer les auteurs des commentaires
# de la section biographie par la première lettre de leur pseudo.
@admin_bp.route("back_end_blog/filtrage_utilisateur_biographie_alphabet", methods=['GET', 'POST'])
def users_biography_alpha_filter():
    """
    Filtre les utilisateurs par la première lettre de leur pseudo et affiche leurs commentaires.

    Cette route permet de filtrer les utilisateurs en fonction de la première lettre de leur pseudo.
    Les utilisateurs filtrés et leurs commentaires sur les biographies sont affichés dans une page HTML.

    Args:
        None

    Returns:
        Response: Une page HTML affichant les utilisateurs filtrés et leurs commentaires sur les biographies.

    Templates:
        admin/users_comments_biography.html: Le modèle utilisé pour rendre la page des commentaires des utilisateurs.

    Context:
        formbiography (CreateMangakaForm): Formulaire pour créer un mangaka.
        user_comments_biography (dict): Dictionnaire contenant les utilisateurs et leurs commentaires sur les biographies.
    """
    formbiography = CreateMangakaForm()

    lettre = request.args.get('lettre', type=str)
    if lettre:
        users = User.query.filter(User.pseudo.ilike(f'{lettre}%')).order_by(
            User.pseudo.asc()).all()
    else:
        users = User.query.order_by(User.pseudo.asc()).all()

    user_comments_biography = {}
    for user in users:
        comments = CommentBiography.query.filter_by(user_id=user.id).all()
        for comment in comments:
            biography = BiographyMangaka.query.get(comment.biography_mangaka_id)
            if user.pseudo not in user_comments_biography:
                user_comments_biography[user.pseudo] = []
            user_comments_biography[user.pseudo].append({
                'biography': biography,
                'comment': comment
            })
    return render_template('admin/users_comments_biography.html', user_comments_biography=user_comments_biography,
                           formbiography=formbiography)


# Route permettant de supprimer le commentaire d'un utilisateur dans la section biographie.
@admin_bp.route("/back_end_blog/supprimer_commentaires_biographie/<int:id>", methods=['GET', 'POST'])
def suppress_biography_comment(id):
    """
    Supprime un commentaire d'une biographie du blog.

    Cette route permet de supprimer un commentaire spécifique, identifié par son ID,
    d'une biographie dans le blog. Après la suppression, un message de confirmation
    est affiché et l'utilisateur est redirigé vers la page de visualisation des commentaires.

    Args:
        id (int): L'identifiant unique du commentaire à supprimer.

    Returns:
        Response: Une redirection vers la page de visualisation des commentaires des utilisateurs
                  après la suppression.

    """

    comment = CommentBiography.query.get_or_404(id)
    if comment:
        # Suppression du commentaire de la biographie.
        db.session.delete(comment)
        # Validation de l'action.
        db.session.commit()
        flash("Le commentaire a été supprimé avec succès." + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))

    return redirect(url_for("admin.users_biography_alpha_filter"))


# Route permettant de chercher une biographie selon le nom du mangaka.
@admin_bp.route("back_end_blog/filtrage_utilisateur_biographie_recherche", methods=['GET', 'POST'])
def biography_search():
    """
    Rechercher des biographies de mangakas par leur nom ou prénom.

    Cette route permet aux utilisateurs de rechercher des biographies en utilisant le nom
    ou le prénom du mangaka. Les résultats de la recherche sont affichés par ordre alphabétique.

    Args:
        None

    Returns:
        Response: Une page HTML avec les résultats de la recherche et les formulaires associés.

    Templates:
        admin/create_mangaka.html: Le modèle utilisé pour rendre la page de recherche.

    Context:
        authors (list): Liste de tous les auteurs disponibles.
        biographies (list): Liste des biographies correspondant à la requête de recherche.
        formuser (CommentBiographyForm): Formulaire pour les commentaires sur les biographies.
        suppressform (SuppressCommentBiographyForm): Formulaire pour supprimer des commentaires de biographies.
        formmangaka (CreateMangakaForm): Formulaire pour créer un mangaka.
        delete_form (DeleteBiographyForm): Formulaire pour supprimer une biographie.
    """
    formuser = CommentBiographyForm()
    suppressform = SuppressCommentBiographyForm()
    formmangaka = CreateMangakaForm()
    delete_form = DeleteBiographyForm()

    authors = Author.query.all()

    search_query = request.args.get('search_query', type=str)
    if search_query:
        biographies = BiographyMangaka.query.filter(
            BiographyMangaka.mangaka_name.ilike(f'%{search_query}%')
        ).order_by(BiographyMangaka.mangaka_name.asc()).all()
    else:
        biographies = []

    return render_template('admin/create_mangaka.html', authors=authors, biographies=biographies, formuser=formuser,
                           suppressform=suppressform, formmangaka=formmangaka, delete_form=delete_form)


# Route permettant de supprimer une biographie des bases de données.
@admin_bp.route("back_end_blog/supprimer_biographie/<int:biography_id>", methods=['POST'])
def delete_biography(biography_id):
    """
    Supprime une biographie de la base de données.

    Cette route permet de supprimer une biographie spécifiée par son ID. Si la biographie
    existe, elle est supprimée de la base de données et un message de confirmation est affiché.
    Si la biographie n'existe pas, une erreur est levée.

    Args:
        biography_id (int): L'identifiant unique de la biographie à supprimer.

    Returns:
        Response: Une redirection vers la page de recherche des biographies avec un message de succès.

    Raises:
        ValueError: Si aucune biographie n'est trouvée avec l'ID fourni.
    """
    biography = BiographyMangaka.query.get_or_404(biography_id)
    if biography:
        db.session.delete(biography)
        db.session.commit()
        flash(f'La biographie de {biography.mangaka_name} a été supprimée.', 'success')
        return redirect(url_for('admin.biography_search'))
    else:
        raise ValueError(f"Aucune biographie trouvée avec l'ID {biography_id}")





