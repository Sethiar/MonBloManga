"""
Code permettant à l'utilisateur d'utiliser le blog.
"""
import os.path

from app.user import user_bp

import bcrypt

from PIL import Image
from io import BytesIO

from flask_login import login_required, current_user
from flask import redirect, url_for, render_template, flash, request, jsonify
from markupsafe import escape

from app.extensions import allowed_file

from app.Models import db

from app.Models.forms import LikeForm, DislikeForm, UserSaving, NewSubjectForumForm,\
    CommentSubjectForm, ReplyArticleForm, ReplySubjectForm, LikeBiographyForm, DislikeBiographyForm, ReplyBiographyForm

from app.Models.articles import Article
from app.Models.comment_article import CommentArticle
from app.Models.comment_subject import CommentSubject

from app.Models.biographies import BiographyMangaka
from app.Models.comment_biography import CommentBiography

from app.Models.user import User
from app.Models.subjects_forum import SubjectForum
from app.Models.reply_article import ReplyArticle
from app.Models.reply_subject import ReplySubject
from app.Models.reply_biography import ReplyBiography

from app.Models.likes import Likes, Dislikes
from app.Models.likes_biography import LikesBiography, DislikesBiography

from app.Models.likes_comment_article import CommentLikeArticle
from app.Models.likes_comment_subject import CommentLikeSubject
from app.Models.likes_comment_biography import CommentLikeBiography


# Route permettant à un nouvel utilisateur de s'inscrire.
@user_bp.route("/enregistrement_membre", methods=['GET', 'POST'])
def user_recording():
    """

    :return:
    """
    form = UserSaving()

    if form.validate_on_submit():
        pseudo = form.pseudo.data
        password_hash = form.password.data
        email = form.email.data
        date_naissance = form.date_naissance.data

        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_hash.encode('utf-8'), salt)

        # Vérifiez si le fichier a été soumis
        if 'profil_photo' not in request.files or request.files['profil_photo'].filename == '':
            print("Aucune photo de profil fournie.", "error")
            return redirect(url_for('user.user_recording'))

        profil_photo = request.files['profil_photo']
        if profil_photo and allowed_file(profil_photo.filename):
            photo_data = profil_photo.read()

            # Utilisation de pillow pour redimensionner l'image.
            try:
                img = Image.open(BytesIO(photo_data))
                img.thumbnail((75, 75))
                img_format = img.format if img.format else 'JPEG'
                output = BytesIO()
                img.save(output, format=img_format)
                photo_data_resized = output.getvalue()
            except Exception as e:
                print(f"Erreur lors du redimensionnement de l'image : {str(e)}", "error")
                return redirect(url_for("user.user_recording"))

            if len(photo_data_resized) > 5 * 1024 * 1024:  # 5 Mo
                print("Le fichier est trop grand (maximum 5 Mo).", "error")
                return redirect(url_for('user.user_recording'))

            photo_data = profil_photo.read()  # Lire les données binaires de l'image
        else:
            print("Type de fichier non autorisé.", "error")
            return redirect(url_for('user.user_recording'))

        new_user = User(
            pseudo=pseudo,
            password_hash=password_hash,
            salt=salt,
            email=email,
            date_naissance=date_naissance,
            profil_photo=photo_data_resized  # Stockez les données binaires de l'image
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            print("Inscription réussie! Vous pouvez maintenant vous connecter.")
            return redirect(url_for("mail.send_confirmation_email", email=email))
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de l'enregistrement de l'utilisateur: {str(e)}", "error")

    return render_template("User/form_user.html", form=form)


@user_bp.route("/profil_photo/<int:user_id>")
def profil_photo(user_id):
    """

    :param user_id:
    :return:
    """
    user = User.query.get_or_404(user_id)
    if user.profil_photo:
        return user.profil_photo, {'Content-Type': 'image/jpeg'}  # Ou 'image/png' selon le format
    else:
        return "No image found", 404


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

    # Récupération des réponses au commentaire.
    reply = ReplyArticle.query.get(comment_article_id)

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

    return redirect(url_for('frontend.show_article', article_id=comment.article_id, reply=reply))


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


# Route permettant de poster un commentaire dans la section biographie une fois connecté.
@user_bp.route("/<string:user_pseudo>/biographie/commentaires", methods=['POST'])
@login_required
def comment_biography(user_pseudo):
    """
    Permet à uin utilisateur de laisser un commentaire sur une biographie.

    Args:
        user_pseudo(str): le pseudo de l'utilisateur.

    Returns:
         Redirige vers la page de la biographie après avoir laissé un commentaire.
    """

    if request.method == 'POST':
        # Obtention de l'id de la biographie à partir de la requête POST.
        biography_mangaka_id = request.form.get("biography_mangaka_id")

        # Obtention de l'utilisateur actuel à partir du pseudo.
        user = User.query.filter_by(pseudo=user_pseudo).first()

        # Vérification de l'existence de l'utilisateur et de la biography.
        if user and biography_mangaka_id:
            # Obtenir le contenu du commentaire à partir de la requête POST.
            comment_content = request.form.get("comment_content")

            # Créer un nouvel objet de commentaire.
            new_comment = CommentBiography(comment_content=comment_content, user_id=user.id, biography_mangaka_id=biography_mangaka_id)

            # Ajouter le nouveau commentaire à la table de données.
            db.session.add(new_comment)
            db.session.commit()

            # Récupération de tous les commentaires de l'article après ajout du commentaire.
            comment_content = CommentBiography.query.filter_by(biography_mangaka_id=biography_mangaka_id).first()

            # Redirection sur la page d'affichage des articles.
            return redirect(url_for("frontend.show_biography", biography_mangaka_id=biography_mangaka_id, comment_content=comment_content))
        else:
            # Redirection vers une autre page si l'utilisateur n'existe pas.
            return redirect(url_for("functional.connection_requise"))


# Route permettant de liker une biographie.
@user_bp.route("/biographie/likes<int:biography_mangaka_id>", methods=['POST'])
@login_required
def biography_like(biography_mangaka_id):
    """

    :param biography_mangaka_id:
    :return:
    """
    # Instanciation des formulaires.
    formlike = LikeBiographyForm()

    if formlike.validate_on_submit():
        # Récupération de la biographie ou de l'error 404 si aucune biographie.
        biography = BiographyMangaka.query.get_or_404(biography_mangaka_id)

        # Vérification si l'utilisateur a déjà liké ou disliké cette biographie.
        existing_like = LikesBiography.query.filter_by(user_id=current_user.id,
                                                       biography_mangaka_id=biography_mangaka_id).first()
        existing_dislike = DislikesBiography.query.filter_by(user_id=current_user.id,
                                                             biography_mangaka_id=biography_mangaka_id).first()

        if existing_like:
            flash("Vous avez déjà liké cette biographie.", "info")
        else:
            if existing_dislike:
                db.session.delete(existing_dislike)
                biography.dislikes -= 1

            # Ajout d'un like.
            new_like = LikesBiography(user_id=current_user.id, biography_mangaka_id=biography_mangaka_id)
            db.session.add(new_like)
            biography.likes += 1

            # Enregistrement dans la base de données.
            db.session.commit()
            flash("Merci pour votre like!", "success")

        # Redirection vers la page de la biographie.
        return redirect(url_for('frontend.show_biography', biography_mangaka_id=biography_mangaka_id))

        # En cas de non-validation du formulaire, redirection avec message d'erreur.
    flash("Erreur lors de la soumission du formulaire.", "danger")
    return redirect(url_for('frontend.show_biography', biography_mangaka_id=biography_mangaka_id))


# Route permettant de disliker une biographie.
@user_bp.route("/biographie/dislikes<int:biography_mangaka_id>", methods=['POST'])
@login_required
def biography_dislike(biography_mangaka_id):
    """

    :param biography_mangaka_id:
    :return:
    """
    # Instanciation des formulaires.
    formdislike = DislikeBiographyForm()

    if formdislike.validate_on_submit():
        # Récupération de la biographie ou de l'error 404 si aucune biographie.
        biography = BiographyMangaka.query.get_or_404(biography_mangaka_id)

        # Vérifiez si l'utilisateur a déjà liké ou disliké cette biographie.
        existing_like = LikesBiography.query.filter_by(user_id=current_user.id,
                                                       biography_mangaka_id=biography_mangaka_id).first()
        existing_dislike = DislikesBiography.query.filter_by(user_id=current_user.id,
                                                             biography_mangaka_id=biography_mangaka_id).first()

        if existing_dislike:
            flash("Vous avez déjà disliké cet article.", "info")
        else:
            if existing_like:
                db.session.delete(existing_like)
                biography.likes -= 1

            # Ajout d'un dislike.
            new_dislike = DislikesBiography(user_id=current_user.id, biography_mangaka_id=biography_mangaka_id)
            db.session.add(new_dislike)
            biography.dislikes += 1

            # Enregistrement dans la base de données.
            db.session.commit()
            flash("Merci pour votre dislike!", "success")

        # Redirection vers la page de l'article.
        return redirect(url_for('frontend.show_biography', biography_mangaka_id=biography_mangaka_id))

        # En cas de non-validation du formulaire, redirection avec message d'erreur.
    flash("Erreur lors de la soumission du formulaire.", "danger")
    return redirect(url_for('frontend.show_biography', biography_mangaka_id=biography_mangaka_id))


# Route permettant de liker un commentaire de la section article.
@user_bp.route("/likes_comment_biographie", methods=['POST'])
@login_required
def likes_comment_biography():
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
        comment = CommentBiography.query.get(comment_id)
        if not comment:
            return jsonify({"status": "error", "message": "Comment not found"}), 404

        like_entry = CommentLikeBiography.query.filter_by(user_id=user_id, comment_id=comment_id).first()

        if like_entry:
            # Suppression d'un like.
            db.session.delete(like_entry)
            db.session.commit()
            liked = False
        else:
            # Ajout d'un like.
            new_like = CommentLikeBiography(user_id=user_id, comment_id=comment_id)
            db.session.add(new_like)
            db.session.commit()
            liked = True

        # Comptage du nombre de likes pour le commentaire des biographies.
        like_count = CommentLikeBiography.query.filter_by(comment_id=comment_id).count()
        # Obtention des IDs des utilisateurs ayant liké le commentaire des biographies.
        liked_user_ids = [like.user_id for like in CommentLikeBiography.query.filter_by(comment_id=comment_id).all()]

        return jsonify({"status": "success",
                        "liked": liked,
                        "like_count": like_count,
                        "user_pseudo": pseudo,
                        "liked_user_ids": liked_user_ids})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Route permettant de répondre à un commentaire de la section biographie une fois connecté.
@user_bp.route("/<string:user_pseudo>/comment<int:comment_biography_id>/reply_biography", methods=['GET', 'POST'])
@login_required
def comment_replies_biography(comment_biography_id, user_pseudo):
    """
    Permet à un utilisateur de laisser une réponse à un commentaire d'une biographie.

    Args:
        comment_biography_id(int): l'identifiant du commentaire.
        user_pseudo(str): le pseudo de l'utilisateur.

    Returns:
         Redirige vers la page de l'article après avoir laissé une réponse.
    """
    # Création de l'instance du formulaire.
    formbiographyreply = ReplyBiographyForm()

    # Récupération du commentaire par son id.
    comment = CommentBiography.query.get(comment_biography_id)

    # Vérification de l'existence du commentaire.
    if not comment:
        flash("Le commentaire n'a pas été trouvé.", "error")
        return redirect(url_for("frontend.show_biography", biography_id=comment.biography_id))

    if formbiographyreply.validate_on_submit():

        # Obtention de l'utilisateur actuel à partir du pseudo.
        user = User.query.filter_by(pseudo=user_pseudo).first()

        # Vérification de l'existence de l'utilisateur.
        if user:
            # Obtenir le contenu du commentaire à partir de la requête POST.
            reply_content = formbiographyreply.reply_content.data

            # Créer un nouvel objet de commentaire.
            new_reply = ReplyBiography(reply_content=reply_content, user_id=user.id, comment_id=comment.id)

            # Ajouter le nouveau commentaire à la table de données.
            db.session.add(new_reply)
            db.session.commit()
            print('la réponse au commentaire à bien été enregistrée.')

            # Redirection sur la page d'affichage des biographies.
            return redirect(url_for("frontend.show_biography", biography_mangaka_id=comment.biography_mangaka_id))
        else:
            # Redirection vers une autre page si l'utilisateur n'existe pas.
            return redirect(url_for("functional.connection_requise"))

    return redirect(url_for('frontend.show_biography', biography_mangaka_id=comment.biography_id))


# Route permettant de joindre le formulaire afin de poster une réponse à un commentaire.
@user_bp.route("/<string:user_pseudo>/comment<int:comment_id>/reply_form_biography", methods=['GET'])
@login_required
def reply_form_biography(comment_id, user_pseudo):
    """
    Affiche le formulaire pour répondre à un commentaire de la section biographie.
    """
    # Création d'une instance du formulaire.
    formbiographyreply = ReplyBiographyForm()
    # Récupération des commentaires.
    comment = db.session.get(CommentBiography, comment_id)
    # Récupération de l'utilisateur connecté.
    user = User.query.filter_by(pseudo=user_pseudo).first()

    return render_template("User/reply_form_biography.html", form=formbiographyreply, comment=comment, user=user)
