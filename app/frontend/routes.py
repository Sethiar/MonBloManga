"""
Code permettant de définir les routes concernant le frontend du blog.
"""
from app.frontend import frontend_bp

from flask import render_template, url_for, redirect, request, abort
from flask_login import login_required, current_user
from datetime import datetime

from app.Models.forms import CommentArticleForm, CommentSubjectForm, LikeForm, DislikeForm, \
    NewSubjectForumForm, CommentLike, CommentBiographyForm, CommentBiographyLike, DislikeBiographyForm,\
    LikeBiographyForm, SuppressCommentForm, SuppressReplySubject, ChangeCommentArticleForm, \
    SuppressCommentArticleForm, ChangeReplyArticle, SuppressReplyArticle, ChangeCommentBiographyForm, \
    SuppressCommentBiographyForm, ChangeReplyBiography, SuppressReplyBiography

from app.Models.author import Author
from app.Models.articles import Article

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
    Route permettant d'accéder à la page des articles du blog.

    Cette route prend en charge les méthodes GET et POST.

    GET :
        Affiche tous les articles disponibles sur le blog.
        Utilise le template HTML 'Presentation/articles.html'.

    POST :
        Valide et traite le formulaire de commentaire soumis.
        Si le formulaire est valide, redirige l'utilisateur vers une autre page.
        Sinon, affiche la liste des articles avec les erreurs de formulaire.

    Returns:
        Template HTML 'Presentation/articles.html' avec la liste des articles et le formulaire de commentaire.

    Raises:
        Aucune exception n'est levée.
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
    Route permettant d'afficher un article spécifique du blog.

    Args:
        article_id (int): L'identifiant unique de l'article à afficher.

    Returns:
        Template HTML 'Presentation/article.html' avec les détails de l'article spécifié.

    Raises:
        404 Error: Si aucun article correspondant à l'ID spécifié n'est trouvé dans la base de données.
    """
    # Création de l'instance du formulaire.
    formcomment = CommentArticleForm()
    formlike = LikeForm()
    formdislike = DislikeForm()
    formlikecomment = CommentLike()
    formchange_article_comment = ChangeCommentArticleForm()
    formsuppress_article_comment = SuppressCommentArticleForm()
    formchange_article_reply = ChangeReplyArticle()
    formsuppress_article_reply = SuppressReplyArticle()

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

    return render_template("Presentation/article.html", article=article, article_id=article_id,
                           formchange_article_comment=formchange_article_comment,
                           formsuppress_article_comment=formsuppress_article_comment,
                           formchange_article_reply=formchange_article_reply,
                           formsuppress_article_reply=formsuppress_article_reply, comments=comments,
                           formcomment=formcomment, formlike=formlike, formdislike=formdislike,
                           formlikecomment=formlikecomment, comment_likes_data=comment_likes_data)


# Route permettant d'archiver les articles selon leur mois d'édition.
@frontend_bp.route("/archive/<int:year>/<int:month>")
def archive(year, month):
    """
        Afficher les articles archivés pour un mois donné.

        Args:
            year (int): L'année des articles à afficher.
            month (int): Le mois des articles à afficher.

        Returns:
            La page des archives avec les articles pour le mois spécifié.
    """
    # Récupérer les articles pour le mois et l'année spécifiés
    start_date = datetime(year, month, 1)
    if month < 12:
        end_date = datetime(year, month + 1, 1)
    else:
        end_date = datetime(year + 1, 1, 1)

    articles = Article.query.filter(Article.date_edition >= start_date, Article.date_edition < end_date).all()

    return render_template("Presentation/archive.html", articles=articles, year=year, month=month)


# Route permettant d'accéder à la page forum du blog.
@frontend_bp.route("/forum", methods=['GET', 'POST'])
def forum():
    """
    Route permettant d'accéder à la page du forum du blog.

    Returns:
        Template HTML 'Presentation/forum.html' affichant la page du forum et ses sujets.
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
    Route permettant d'accéder à un sujet spécifique du forum.

    Args:
        subject_id (int): L'identifiant du sujet à afficher.

    Returns:
        Template HTML 'Presentation/subject_forum.html' avec les détails du sujet et ses commentaires associés.

    Raises:
        404 Error: Si aucun sujet correspondant à l'ID spécifié n'est trouvé dans la base de données.
    """
    # Création de l'instance de formulaire.
    formcomment = CommentSubjectForm()
    formlikecomment = CommentLike()
    formsuppress = SuppressCommentForm()
    formsuppressreply = SuppressReplySubject()

    # Récupération du sujet spécifié par subject_id depuis la base de données.
    subject = SubjectForum.query.get_or_404(subject_id)

    # Vérification de l'existence du sujet.
    if not subject:
        # Si le sujet n'existe pas, erreur 404 renvoyée.
        abort(404)

    # Récupération des commentaires associés à ce sujet.
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
                           comment_subject=comment_subject, formcomment=formcomment, formsuppress=formsuppress,
                           formsuppressreply=formsuppressreply, formlikecomment=formlikecomment,
                           comment_likes_data=comment_likes_data)


# Route permettant d'accéder à la page Mangaka du blog.
@frontend_bp.route("/biographie-mangaka")
def biography():
    """
    Route permettant d'accéder à la page de la biographie des mangakas.

    Returns:
        Template HTML 'Presentation/biography.html' affichant la biographie des mangakas.
    """
    biographies = BiographyMangaka.query.all()

    return render_template("Presentation/biography.html", biographies=biographies)


@frontend_bp.route("/biographie-mangaka/<int:biography_mangaka_id>", methods=['GET', 'POST'])
@login_required
def show_biography(biography_mangaka_id):
    """
    Route permettant d'afficher la biographie détaillée d'un mangaka.

    Args:
        biography_mangaka_id (int): L'identifiant unique de la biographie de mangaka à afficher.

    Returns:
        Template HTML 'Presentation/biography_mangaka.html' avec les détails de la biographie spécifiée.

    Raises:
        404 Error: Si aucune biographie correspondant à l'ID spécifié n'est trouvée dans la base de données.
    """
    formcomment = CommentBiographyForm()
    formdislike = DislikeForm()
    formlike = LikeBiographyForm()
    formlikecomment = CommentBiographyLike()
    formchange_biography_comment = ChangeCommentBiographyForm()
    formsuppress_biography_comment = SuppressCommentBiographyForm()
    formchange_biography_reply = ChangeReplyBiography()
    formsuppress_biography_reply = SuppressReplyBiography()

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
                           formcomment=formcomment,  formchange_biography_comment=formchange_biography_comment,
                           formsuppress_biography_comment=formsuppress_biography_comment,
                           formchange_biography_reply=formchange_biography_reply,
                           formsuppress_biography_reply=formsuppress_biography_reply, formlike=formlike,
                           formdislike=formdislike, formlikecomment=formlikecomment,
                           comment_likes_data=comment_likes_data)
