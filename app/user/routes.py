"""
Code permettant à l'utilisateur d'utiliser le blog.
"""

from app.user import user_bp

import bcrypt

from flask_login import login_required, current_user
from flask import redirect, url_for, render_template, flash, request, jsonify
from markupsafe import escape

from Models import db
from Models.forms import LikeForm, DislikeForm, UserSaving, NewSubjectForumForm,\
    CommentSubjectForm, ReplyArticleForm, ReplySubjectForm

from Models.articles import Article
from Models.comment_article import CommentArticle
from Models.comment_subject import CommentSubject
from Models.user import User
from Models.subjects_forum import SubjectForum
from Models.reply_article import ReplyArticle
from Models.reply_subject import ReplySubject
from Models.likes import Likes, Dislikes
from Models.likes_comment_article import CommentLikeArticle
from Models.likes_comment_subject import CommentLikeSubject


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
        new_user = User(pseudo=pseudo,
                        password_hash=password_hash,
                        salt=salt,
                        email=email,
                        date_naissance=date_naissance)
        db.session.add(new_user)
        db.session.commit()

        flash("Inscription réussie! Vous pouvez maintenant vous connecter.")

        # Redirection vers la route pour envoyer l'e-mail de confirmation
        return redirect(url_for("mail.send_confirmation_email", email=email))

    return render_template("User/form_user.html", form=form)


# Route permettant de liker un article.
@user_bp.route("/article/likes<int:article_id>", methods=['POST'])
@login_required
def article_like(article_id):
    """

    :param article_id:
    :return:
    """
    # Instanciation des formulaires.
    formlike = LikeForm()

    if formlike.validate_on_submit():
        # Récupération de l'article ou de l'error 404 si aucun article.
        article = Article.query.get_or_404(article_id)

        # Vérifiez si l'utilisateur a déjà liké ou disliké cet article
        existing_like = Likes.query.filter_by(user_id=current_user.id, article_id=article_id).first()
        existing_dislike = Dislikes.query.filter_by(user_id=current_user.id, article_id=article_id).first()

        if existing_like:
            flash("Vous avez déjà liké cet article.", "info")
        else:
            if existing_dislike:
                db.session.delete(existing_dislike)
                article.dislikes -= 1

            # Ajout d'un like.
            new_like = Likes(user_id=current_user.id, article_id=article_id)
            db.session.add(new_like)
            article.likes += 1

            # Enregistrement dans la base de données.
            db.session.commit()
            flash("Merci pour votre like!", "success")

        # Redirection vers la page de l'article.
        return redirect(url_for('frontend.show_article', article_id=article_id))

        # En cas de non-validation du formulaire, redirection avec message d'erreur.
    flash("Erreur lors de la soumission du formulaire.", "danger")
    return redirect(url_for('frontend.show_article', article_id=article_id))


# Route permettant de disliker un article.
@user_bp.route("/article/dislikes<int:article_id>", methods=['POST'])
@login_required
def article_dislike(article_id):
    """

    :param article_id:
    :return:
    """
    # Instanciation des formulaires.
    formdislike = DislikeForm()

    if formdislike.validate_on_submit():
        # Récupération de l'article ou de l'error 404 si aucun article.
        article = Article.query.get_or_404(article_id)

        # Vérifiez si l'utilisateur a déjà liké ou disliké cet article
        existing_like = Likes.query.filter_by(user_id=current_user.id, article_id=article_id).first()
        existing_dislike = Dislikes.query.filter_by(user_id=current_user.id, article_id=article_id).first()

        if existing_dislike:
            flash("Vous avez déjà disliké cet article.", "info")
        else:
            if existing_like:
                db.session.delete(existing_like)
                article.likes -= 1

            # Ajout d'un dislike.
            new_dislike = Dislikes(user_id=current_user.id, article_id=article_id)
            db.session.add(new_dislike)
            article.dislikes += 1

            # Enregistrement dans la base de données.
            db.session.commit()
            flash("Merci pour votre dislike!", "success")

        # Redirection vers la page de l'article.
        return redirect(url_for('frontend.show_article', article_id=article_id))

        # En cas de non-validation du formulaire, redirection avec message d'erreur.
    flash("Erreur lors de la soumission du formulaire.", "danger")
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
@user_bp.route("/<string:user_pseudo>/article/commentaires", methods=['POST'])
@login_required
def comment_article(user_pseudo):
    """
    Permet à uin utilisateur de laisser un commentaire sur un article.

    Args:
        user_pseudo(str): le pseudo de l'utilisateur.

    Returns:
         Redirige vers al page de l'article après avoir laissé un commentaire.
    """

    if request.method == 'POST':
        # Obtention de l'id de l'article à partir de la requête POST.
        article_id = request.form.get("article_id")

        # Obtention de l'utilisateur actuel à partir du pseudo.
        user = User.query.filter_by(pseudo=user_pseudo).first()

        # Vérification de l'existence de l'utilisateur et de l'article.
        if user and article_id:
            # Obtenir le contenu du commentaire à partir de la requête POST.
            comment_content = request.form.get("comment_content")

            # Créer un nouvel objet de commentaire.
            new_comment = CommentArticle(comment_content=comment_content, user_id=user.id, article_id=article_id)

            # Ajouter le nouveau commentaire à la table de données.
            db.session.add(new_comment)
            db.session.commit()

            # Récupération de tous les commentaires de l'article après ajout du commentaire.
            comment_content = CommentArticle.query.filter_by(article_id=article_id).first()

            # Redirection sur la page d'affichage des articles.
            return redirect(url_for("frontend.show_article", article_id=article_id, comment_content=comment_content))
        else:
            # Redirection vers une autre page si l'utilisateur n'existe pas.
            return redirect(url_for("functional.connection_requise"))


# Route permettant de liker un commentaire de la section article.
@user_bp.route("/likes_comment_article", methods=['POST'])
@login_required
def likes_comment_article():
    """

    :return:
    """
    data = request.get_json()
    comment_id = data.get("comment_id")
    pseudo = current_user.pseudo

    if not comment_id or not pseudo:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    try:
        user = User.query.filter_by(pseudo=pseudo).one()
        user_id = user.id
        comment = CommentArticle.query.get(comment_id)
        if not comment:
            return jsonify({"status": "error", "message": "Comment not found"}), 404

        like_entry = CommentLikeArticle.query.filter_by(user_id=user_id, comment_id=comment_id).first()

        if like_entry:
            # Suppression d'un like.
            db.session.delete(like_entry)
            db.session.commit()
            liked = False
        else:
            # Ajout d'un like.
            new_like = CommentLikeArticle(user_id=user_id, comment_id=comment_id)
            db.session.add(new_like)
            db.session.commit()
            liked = True

        # Comptage du nombre de likes pour le commentaire des articles.
        like_count = CommentLikeArticle.query.filter_by(comment_id=comment_id).count()
        # Obtention des IDs des utilisateurs ayant liké le commentaire des articles.
        liked_user_ids = [like.user_id for like in CommentLikeArticle.query.filter_by(comment_id=comment_id).all()]

        return jsonify({"status": "success",
                        "liked": liked,
                        "like_count": like_count,
                        "user_pseudo": pseudo,
                        "liked_user_ids": liked_user_ids})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Route permettant de répondre à un commentaire de la section article une fois connecté.
@user_bp.route("/<string:user_pseudo>/comment<int:comment_article_id>/reply_article", methods=['GET', 'POST'])
@login_required
def comment_replies_article(comment_article_id, user_pseudo):
    """
    Permet à un utilisateur de laisser une réponse à un commentaire d'un article.

    Args:
        comment_article_id(int): l'identifiant du commentaire.
        user_pseudo(str): le pseudo de l'utilisateur.

    Returns:
         Redirige vers la page de l'article après avoir laissé une réponse.
    """
    # Création de l'instance du formulaire.
    formarticlereply = ReplyArticleForm()

    # Récupération du commentaire par son id.
    comment = CommentArticle.query.get(comment_article_id)

    # Vérification de l'existence du commentaire.
    if not comment:
        flash("Le commentaire n'a pas été trouvé.", "error")
        return redirect(url_for("frontend.show_article", article_id=comment.article_id))

    if formarticlereply.validate_on_submit():

        # Obtention de l'utilisateur actuel à partir du pseudo.
        user = User.query.filter_by(pseudo=user_pseudo).first()

        # Vérification de l'existence de l'utilisateur.
        if user:
            # Obtenir le contenu du commentaire à partir de la requête POST.
            reply_content = formarticlereply.reply_content.data

            # Créer un nouvel objet de commentaire.
            new_reply = ReplyArticle(reply_content=reply_content, user_id=user.id, comment_id=comment.id)

            # Ajouter le nouveau commentaire à la table de données.
            db.session.add(new_reply)
            db.session.commit()
            print('la réponse au commentaire à bien été enregistrée.')

            # Redirection sur la page d'affichage des articles.
            return redirect(url_for("frontend.show_article", article_id=comment.article_id))
        else:
            # Redirection vers une autre page si l'utilisateur n'existe pas.
            return redirect(url_for("functional.connection_requise"))

    return redirect(url_for('frontend.show_article', article_id=comment.article_id))


# Route permettant de joindre le formulaire afin de poster une réponse à un commentaire.
@user_bp.route("/<string:user_pseudo>/comment<int:comment_id>/reply_form_article", methods=['GET'])
@login_required
def reply_form_article(comment_id, user_pseudo):
    """
    Affiche le formulaire pour répondre à un commentaire.
    """
    # Création d'une instance du formulaire.
    formarticlereply = ReplyArticleForm()
    # Récupération des commentaires.
    comment = db.session.get(CommentArticle, comment_id)
    # Récupération de l'utilisateur connecté.
    user = User.query.filter_by(pseudo=user_pseudo).first()

    return render_template("User/reply_form_article.html", form=formarticlereply, comment=comment, user=user)


# Route permettant de commenter un sujet du forum.
@user_bp.route("/<string:user_pseudo>/forum/commentaires_sujet", methods=['POST'])
@login_required
def comment_subject(user_pseudo):
    """
    Permet à un utilisateur de laisser un commentaire sur un sujet du forum.

    Args:
        user_pseudo(str): le pseudo de l'utilisateur.

    Returns:
         Redirige vers la page du forum dédiée au sujet après avoir laissé un commentaire.
    """
    # Création de l'instance du formulaire.
    formcomment = CommentSubjectForm()

    if request.method == 'POST':

        # Obtention de l'id du sujet du forum à partir de la requête POST.
        subject_id = request.form.get("subject_id")

        # Obtention de l'utilisateur actuel à partir du pseudo.
        user = User.query.filter_by(pseudo=user_pseudo).first()

        # Vérification de l'existence de l'utilisateur et du sujet.
        if user and subject_id:
            # Obtenir le contenu du commentaire à partir de la requête POST.
            comment_content = request.form.get("comment_content")

            # Créer un nouvel objet de commentaire.
            new_comment = CommentSubject(comment_content=comment_content, user_id=user.id, subject_id=subject_id)

            # Ajouter le nouveau commentaire à la table de données.
            db.session.add(new_comment)
            db.session.commit()

            # Récupération de tous les commentaires du sujet après ajout du commentaire.
            comment_content = CommentSubject.query.filter_by(subject_id=subject_id).first()

            # Redirection sur la page d'affichage des sujets.
            return redirect(url_for("frontend.forum_subject", subject_id=subject_id, comment_content=comment_content))
        else:
            # Redirection vers une autre page si l'utilisateur ou le sujet n'existe pas.
            return redirect(url_for("functional.connection_requise"))


# Route permettant de répondre à un commentaire une fois connecté.
@user_bp.route("/<string:user_pseudo>/comment<int:comment_subject_id>/reply_subject", methods=['GET', 'POST'])
@login_required
def comment_replies_subject(comment_subject_id, user_pseudo):
    """
    Permet à un utilisateur de laisser une réponse à un commentaire à un sujet du forum.

    Args:
        comment_subject_id(int): l'identifiant du commentaire.
        user_pseudo(str): le pseudo de l'utilisateur.

    Returns:
         Redirige vers la page du forum après avoir laissé une réponse.
    """
    # Création de l'instance du formulaire.
    formsubjectreply = ReplySubjectForm()

    # Récupérer le commentaire par son id.
    comment = CommentSubject.query.get(comment_subject_id)

    if not comment:
        flash("Le commentaire n'a pas été trouvé.", "error")
        return redirect(url_for("frontend.forum"))

    if formsubjectreply.validate_on_submit():
        # Obtention de l'utilisateur actuel à partir du pseudo.
        user = User.query.filter_by(pseudo=user_pseudo).first()

        if not user:
            flash("Utilisateur non trouvé.", "error")
            return redirect(url_for("functional.connection_requise"))

        # Obtenir le contenu du commentaire à partir de la requête POST.
        reply_content = formsubjectreply.reply_content.data

        # Obtenir l'ID du commentaire parent à partir du formulaire
        comment_id = formsubjectreply.comment_id.data

        # Créer une nouvelle réponse au commentaire.
        new_reply = ReplySubject(reply_content=reply_content, user_id=user.id, comment_id=comment_id)

        # Ajouter le nouveau commentaire à la table de données.
        db.session.add(new_reply)
        db.session.commit()

        flash("La réponse au commentaire a bien été enregistrée.", "success")

        # Redirection vers la page du sujet du forum
        return redirect(url_for("frontend.forum_subject", subject_id=comment.subject_id))

    # Si le formulaire n'est pas validé ou en méthode GET, affichez le formulaire de réponse
    return render_template("reply_form_subject.html", form=formsubjectreply, comment=comment)


# Route permettant de liker un commentaire dans la section forum.
@user_bp.route("/likes_comment_subject", methods=['POST'])
@login_required
def likes_comment_subject():
    """

    :return:
    """
    data = request.get_json()
    comment_id = data.get("comment_id")
    pseudo = current_user.pseudo

    if not comment_id or not pseudo:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    try:
        user = User.query.filter_by(pseudo=pseudo).one()
        user_id = user.id
        comment = CommentSubject.query.get(comment_id)
        if not comment:
            return jsonify({"status": "error", "message": "Comment not found"}), 404

        like_entry = CommentLikeSubject.query.filter_by(user_id=user_id, comment_id=comment_id).first()

        if like_entry:
            # Suppression d'un like.
            db.session.delete(like_entry)
            db.session.commit()
            liked = False
        else:
            # Ajout d'un like.
            new_like = CommentLikeSubject(user_id=user_id, comment_id=comment_id)
            db.session.add(new_like)
            db.session.commit()
            liked = True

        # Comptage du nombre de likes pour le commentaire.
        like_count = CommentLikeSubject.query.filter_by(comment_id=comment_id).count()
        # Obtention des IDs des utilisateurs ayant liké le commentaire.
        liked_user_ids = [like.user_id for like in CommentLikeSubject.query.filter_by(comment_id=comment_id).all()]

        return jsonify({"status": "success",
                        "liked": liked,
                        "like_count": like_count,
                        "user_pseudo": pseudo,
                        "liked_user_ids": liked_user_ids})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Route permettant de joindre le formulaire afin de poster une réponse à un commentaire.
@user_bp.route("/<string:user_pseudo>/comment<int:comment_id>/reply_form_subject", methods=['GET'])
@login_required
def reply_form_subject(comment_id, user_pseudo):
    """
    Affiche le formulaire pour répondre à un commentaire.
    """
    # Création d'une instance du formulaire.
    formsubjectreply = ReplySubjectForm()
    # Récupération des commentaires du sujet.
    comment = db.session.get(CommentSubject, comment_id)
    # Récupération des utilisateurs qui ont posté sur le sujet.
    user = User.query.filter_by(pseudo=user_pseudo).first()

    return render_template("User/reply_form_subject.html", formsubjectreply=formsubjectreply,
                           comment=comment, user=user)


# Route permettant de liker un commentaire une fois connecté.
@user_bp.route("/like_comment/<int:comment_id>", methods=['POST'])
def comment_like(comment_id):
    """

    :param comment_id:
    :return:
    """
    # Récupération des commentaires.
    comment = CommentArticle.query.get_or_404(comment_id)
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
    comment = CommentArticle.query.get_or_404(comment_id)
    # Ajout d'un dislike.
    comment.dislikes += 1
    # Enregistrement dans la base de données.
    db.session.commit()

    return redirect(url_for('frontend.show_article'))

