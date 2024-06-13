"""
Code permettant de définir les routes concernant le frontend du blog.
"""
from app.frontend import frontend_bp

from flask import render_template, url_for, redirect, request, abort
from flask_login import login_required, current_user


from app.Models.forms import CommentArticleForm, CommentSubjectForm, LikeForm, DislikeForm, \
    NewSubjectForumForm, CommentLike, CommentBiographyForm, CommentBiographyLike, DislikeBiographyForm,\
    LikeBiographyForm

from app.Models.author import Author
from app.Models.articles import Article
from app.Models.biographies import BiographyMangaka

from app.Models.comment_article import CommentArticle
from app.Models.comment_subject import CommentSubject
from app.Models.comment_biography import CommentBiography

from app.Models.likes_comment_subject import CommentLikeSubject
from app.Models.likes_comment_article import CommentLikeArticle
from app.Models.likes_comment_biography import CommentLikeBiography


from app.Models.subjects_forum import SubjectForum
from app.Models.biographies import BiographyMangaka


# Route permettant d'accéder à la page article du blog.
@frontend_bp.route("/articles", methods=['GET', 'POST'])
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
    form = CommentArticleForm()

    if request.method == 'POST':
        # Validation du formulaire du commentaire.
        if form.validate_on_submit():
            # Récupération du pseudo de l'utilisateur depuis le formulaire.
            user_pseudo = form.pseudo_user.data
            return redirect(url_for("user.comment_article", user_pseudo=user_pseudo))
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


# Route permettant d'accéder à la lecture d'un article en particulier du blog.
@frontend_bp.route("/article/<int:article_id>")
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
    formcomment = CommentArticleForm()
    formlike = LikeForm()
    formdislike = DislikeForm()
    formlikecomment = CommentLike()

    # Récupération de l'article depuis la base de données en utilisant son id.
    article = Article.query.get_or_404(article_id)

    # Vérifier si l'article existe.
    if not article:
        # Si l'article n'existe pas, renvoyer une erreur 404.
        abort(404)

    # Récupération des commentaires associés à cet article.
    comment_article = CommentArticle.query.filter_by(article_id=article_id).all()

    # Préparation des données de likes pour chaque commentaire.
    comment_likes_data = {}
    for comment in comment_article:
        like_count = CommentLikeArticle.query.filter_by(comment_id=comment.id).count()
        liked_user_ids = [like.user_id for like in CommentLikeArticle.query.filter_by(comment_id=comment.id).all()]
        liked_by_current_user = current_user.id in liked_user_ids
        comment_likes_data[comment.id] = {
            "like_count": like_count,
            "liked_user_ids": liked_user_ids,
            "liked_by_current_user": liked_by_current_user
        }

    # Récupération des commentaires associés à cet article.
    comments = CommentArticle.query.filter_by(article_id=article_id).all()

    return render_template("Presentation/article.html", article=article, article_id=article_id, comments=comments,
                           formcomment=formcomment, formlike=formlike, formdislike=formdislike,
                           formlikecomment=formlikecomment, comment_likes_data=comment_likes_data)


# Route permettant d'accéder à la page forum du blog.
@frontend_bp.route("/forum", methods=['GET', 'POST'])
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


@frontend_bp.route("/forum/<int:subject_id>", methods=['GET', 'POST'])
@login_required
def forum_subject(subject_id):
    """
    Page permettant d'échanger sur un sujet émis par la communauté.

    Args:
        subject_id (int): L'identifiant du sujet à afficher.

    Returns:
        La page de discussion sur le sujet spécifié.
    """

    # Création de l'instance de formulaire.
    formcomment = CommentSubjectForm()
    formlikecomment = CommentLike()

    # Récupération du sujet spécifié par subject_id depuis la base de données.
    subject = SubjectForum.query.get_or_404(subject_id)

    # Vérifier si l'article existe.
    if not subject:
        # Si l'article n'existe pas, renvoyer une erreur 404.
        abort(404)

    # Récupération des commentaires associés à cet article.
    comment_subject = CommentSubject.query.filter_by(subject_id=subject_id).all()

    # Préparation des données de likes pour chaque commentaire.
    comment_likes_data = {}
    for comment in comment_subject:
        like_count = CommentLikeSubject.query.filter_by(comment_id=comment.id).count()
        liked_user_ids = [like.user_id for like in CommentLikeSubject.query.filter_by(comment_id=comment.id).all()]
        liked_by_current_user = current_user.id in liked_user_ids
        comment_likes_data[comment.id] = {
            "like_count": like_count,
            "liked_user_ids": liked_user_ids,
            "liked_by_current_user": liked_by_current_user
        }

    return render_template("Presentation/subject_forum.html", subject=subject, subject_id=subject_id,
                           comment_subject=comment_subject, formcomment=formcomment, formlikecomment=formlikecomment,
                           comment_likes_data=comment_likes_data)


# Route permettant d'accéder à la page Mangaka du blog.
@frontend_bp.route("/biographie_mangaka")
def biography():
    """
    Accès à la page de la biographie des mangakas.

    Returns :
    La page des Mangakas.
    """

    biographies = BiographyMangaka.query.all()

    return render_template("Presentation/biography.html", biographies=biographies)


@frontend_bp.route("/biographie_mangaka/<int:biography_mangaka_id>", methods=['GET', 'POST'])
def show_biography(biography_mangaka_id):
    """
    Route permettant de visualiser une biographie de mangaka en particulier.

    :param biography_mangaka_id:
    :return:
    """
    formcomment = CommentBiographyForm()
    formdislike = DislikeForm()
    formlike = LikeBiographyForm()
    formlikecomment = CommentBiographyLike()

    # Récupération de la biographie si elle existe.
    biography = BiographyMangaka.query.get_or_404(biography_mangaka_id)

    # Vérification de l'existence de la biographie.
    if not biography:
        # Si l'article n'existe pas, renvoyer une erreur 404.
        abort(404)

    # Récupération des commentaires associés à cette biographie.
    comment_biography = CommentBiography.query.filter_by(biography_mangaka_id=biography_mangaka_id).all()

    # Préparation des données de likes pour chaque commentaire.
    comment_likes_data = {}
    for comment in comment_biography:
        like_count = CommentLikeBiography.query.filter_by(comment_id=comment.id).count()
        liked_user_ids = [like.user_id for like in CommentLikeBiography.query.filter_by(comment_id=comment.id).all()]
        liked_by_current_user = current_user.id in liked_user_ids
        comment_likes_data[comment.id] = {
            "like_count": like_count,
            "liked_user_ids": liked_user_ids,
            "liked_by_current_user": liked_by_current_user
        }

    # Récupération des commentaires associés à cette biographie.
    comments = CommentBiography.query.filter_by(biography_mangaka_id=biography_mangaka_id).all()

    return render_template("Presentation/biography_mangaka.html", biography=biography,
                           biography_mangaka_id=biography_mangaka_id, comments=comments,
                           formcomment=formcomment, formlike=formlike, formdislike=formdislike,
                           formlikecomment=formlikecomment, comment_likes_data=comment_likes_data)
