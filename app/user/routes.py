"""

"""

import bcrypt

from datetime import datetime

from flask_login import login_required

from flask import redirect, url_for, render_template, flash, request

from markupsafe import escape

from Models import db

from Models.forms import LikeForm, DislikeForm, CommentForm, UserSaving, ReplyForm, NewSubjectForumForm

from Models.articles import Article
from Models.comment import Comment
from Models.user import User
from Models.subjects_forum import SubjectForum
from Models.reply import Reply

from app.user import user_bp


# Route permettant à un nouvel utilisateur de s'inscrire.
@user_bp.route("/enregistrement_membre", methods=['GET', 'POST'])
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
        return redirect(url_for("frontend.landing_page"))

    return render_template("User/form_user.html", form=form)


# Route permettant de liker un article.
@user_bp.route("/article/likes<int:article_id>", methods=['POST'])
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
        return redirect(url_for('frontend.show_article', article_id=article_id))


# Route permettant de disliker un article.
@user_bp.route("/article/dislikes<int:article_id>", methods=['POST'])
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
    return redirect(url_for('frontend.show_article', article_id=article_id))


# Route permettant d'ajouter un sujet au forum une fois connecté.
@user_bp.route("/forum/ajouter_sujet", methods=['POST'])
@login_required
def add_subject_forum():
    """
    Permet de créer un nouveau sujet pour le forum.

    Returns :
        Redirige vers la page du forum.
    """
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


# Route permettant de poster un commentaire une fois connecté.
@user_bp.route("/<string:user_pseudo>/commentaires", methods=['POST'])
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
            return redirect(url_for("frontend.show_article", article_id=article_id, comment_content=comment_content))
        else:
            # Redirection vers une autre page si l'utilisateur n'existe pas.
            return redirect(url_for("functional.connection_requise"))


# Route permettant de liker un commentaire une fois connecté.
@user_bp.route("/like_comment/<int:comment_id>", methods=['POST'])
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

    return redirect(url_for('frontend.show_article'))


# Route permettant de disliker un commentaire une fois connecté.
@user_bp.route("/dislike_comment/<int:comment_id>", methods=['POST'])
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

    return redirect(url_for('frontend.show_article'))


# Route permettant de joindre le formulaire afin de poster une réponse à un commentaire.
@user_bp.route("/<string:user_pseudo>/comment<int:comment_id>/reply_form", methods=['GET'])
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


# Route permettant de répondre à un commentaire une fois connecté.
@user_bp.route("/<string:user_pseudo>/comment<int:comment_id>/reply", methods=['GET', 'POST'])
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
                return redirect(url_for("frontend.show_article", article_id=article_id))
            else:
                # Redirection vers une autre page si l'utilisateur n'existe pas.
                return redirect(url_for("functional.connection_requise"))

    return redirect(url_for('frontend.show_article', article_id=article_id))

