"""Modèles des formulaires"""

from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, HiddenField, \
    EmailField, DateField, SubmitField, TextAreaField, SelectField, FileField

from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileRequired
from app.Models.user import User


# Formulaire permettant la connexion administrateur.
class AdminConnection(FlaskForm):
    """
    Formulaire de connexion pour les administrateurs du site.

    Attributes :
        identifiant (StringField) : Champ pour l'identifiant de l'administrateur.
        role (StringField): Champ pour le rôle de l'administrateur.
        password (PasswordField) : Champ pour le mot de passe de l'administrateur.
        submit (SubmitField): Bouton de soumission du formulaire.
        csrf_token (HiddenField) : Jeton CSRF pour la sécurité du formulaire.

    Example :
        form = AdminConnection()
    """

    identifiant = StringField("Identifiant Administrateur", validators=[DataRequired()],
                              render_kw={"placeholder": "Veuillez renseigner votre identifiant Administrateur."})
    role = StringField("Rôle Administrateur", validators=[DataRequired()],
                       render_kw={"placeholder": "Veuillez renseigner votre rôle Administrateur."})
    password = PasswordField("Mot de passe Administrateur", validators=[DataRequired()],
                             render_kw={"placeholder": "Veuiller renseigner votre mot de passe Administrateur."})
    submit = SubmitField("Se connecter")
    csrf_token = HiddenField()


# Formulaire permettant d'enregistrer un utilisateur.
class UserSaving(FlaskForm):
    """
    Formulaire d'inscription pour les utilisateurs du site.

    Attributes:
        email (EmailField): Champ pour l'adresse e-mail de l'utilisateur.
        pseudo (StringField) : Champ pour le pseudo unique de l'utilisateur.
        password (PasswordField) : Champ pour le mot de passe de l'utilisateur.
        password2 (PasswordField) : Champ pour la confirmation du mot de passe de l'utilisateur.
        profil_photo (FileField) : Champ pour télécharger la photo de profil de l'utilisateur.
        date_naissance (DateField) : Champ pour la date de naissance de l'utilisateur.
        submit (SubmitField): Bouton de soumission du formulaire.
        csrf_token (HiddenField) : Jeton CSRF pour la sécurité du formulaire.

    Example:
        form = UserSaving()
    """

    email = EmailField(
        "Email",
        validators=[DataRequired()],
        render_kw={"placeholder": "Entrez votre email"})
    pseudo = StringField(
        "Pseudo",
        validators=[DataRequired()],
        render_kw={"placeholder": "Entrez votre pseudo personnel"})
    password = PasswordField(
        "Mot de passe Utilisateur",
        validators=[DataRequired()],
        render_kw={"placeholder": "Veuiller renseigner votre mot de passe Utilisateur."})

    password2 = PasswordField(
        "Confirmer le mot de passe",
        validators=[DataRequired(), EqualTo('password', message='Les mots de passe doivent correspondre.')],
        render_kw={"placeholder": "Veuillez confirmer votre mot de passe utilisateur."}
    )
    date_naissance = DateField(
        "Date de naissance",
        validators=[DataRequired()])
    profil_photo = FileField("Photo de profil souhaitée :",
                             validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], "Images only !!")])

    submit = SubmitField(
        "Souscrire aux conditions générales du blog.")

    csrf_token = HiddenField()

    # Fonction qui vérifie si le pseudo existe déjà.
    def validate_pseudo(self, pseudo):
        """
        Valide que le pseudo choisi n'existe pas déjà dans la base de données des utilisateurs.

        Args :
            pseudo (StringField): Pseudo à valider.

        Raises :
            ValidationError : Si le pseudo est déjà utilisé.

        """
        user = User.query.filter_by(pseudo=pseudo.data).first()
        if user:
            raise ValidationError('Ce pseudo est déjà utilisé. Veuillez en choisir un autre.')

    # Fonction qui vérifie si l'email existe déjà.
    def validate_email(self, email):
        """
        Valide que l'adresse e-mail n'existe pas déjà dans la base de données des utilisateurs.

        Args :
            email (EmailField): Adresse e-mail à valider.

        Raises :
            ValidationError : Si l'e-mail est déjà utilisé.

        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Cet email est déjà utilisé. Utilisez un autre email.')

    def __repr__(self):
        return f"UserSaving(pseudo='{self.pseudo}', email='{self.email.data}', date de naissance='{self.date_naissance}')"


# Formulaire permettant l'enregistrement d'un auteur.
class NewAuthor(FlaskForm):
    """
    Formulaire d'enregistrement d'un nouvel auteur.

    Attributes :
        nom (StringField) : Champ pour le nom de l'auteur.
        prenom (StringField) : Champ pour le prénom de l'auteur.
        pseudo (StringField) : Champ pour le pseudo de l'auteur.
        submit (SubmitField) : Bouton de soumission du formulaire.
        csrf_token (HiddenField) : Jeton CSRF pour la sécurité du formulaire.

    Example :
        form = NewAuthor()
    """
    nom = StringField("Nom", validators=[DataRequired()], render_kw={"placeholder": "Veuillez renseigner votre nom."})
    prenom = StringField("Prénom", validators=[DataRequired()],
                         render_kw={"placeholder": "Veuillez renseigner votre prénom."})
    pseudo = StringField("Pseudo", validators=[DataRequired()],
                         render_kw={"placeholder": "Veuillez renseigner votre pseudo."})
    # Action de soumettre le formulaire.
    submit = SubmitField("Ajouter un auteur")
    csrf_token = HiddenField()

    def __repr__(self):
        return f"NewAuthor(pseudo='{self.pseudo}')"


# Formulaire permettant l'authentification d'un utilisateur.
class UserConnection(FlaskForm):
    """
    Formulaire de connexion pour les utilisateurs du site.

    Attributes :
        pseudo (StringField) : Champ pour le pseudo de l'utilisateur.
        password (PasswordField) : Champ pour le mot de passe de l'utilisateur.
        submit (SubmitField): Bouton de soumission du formulaire.
        csrf_token (HiddenField) : Jeton CSRF pour la sécurité du formulaire.

    Example
        form = UserConnection()
    """
    pseudo = StringField("Pseudo", validators=[DataRequired()],
                         render_kw={"placeholder": "Veuillez renseigner votre pseudo."})
    password = PasswordField("Mot de passe", validators=[DataRequired()],
                             render_kw={"placeholder": "Veuillez renseigner votre mot de passe."})
    csrf_token = HiddenField()
    # Action de soumettre le formulaire.
    submit = SubmitField("se connecter")


# Formulaire permettant de bannir un utilisateur.
class BanUserForm(FlaskForm):
    """
    Formulaire permettant de bannir un utilisateur.

    Attributes :
        csrf_token (HiddenField) : Jeton CSRF pour la sécurité du formulaire.
        submit (SubmitField): Bouton de soumission du formulaire.

    Example:
        form = BanUserForm()

        """
    csrf_token = HiddenField()

    # Action de soumettre le formulaire.
    submit = SubmitField('Bannir')


# Formulaire permettant de bannir un utilisateur.
class UnBanUserForm(FlaskForm):
    """
    Formulaire permettant de débannir un utilisateur.

    Attributes :
        csrf_token (HiddenField) : Jeton CSRF pour la sécurité du formulaire.
        submit (SubmitField): Bouton de soumission du formulaire.

    Example:
        form = UnBanUserForm()
    """
    csrf_token = HiddenField()

    # Action de soumettre le formulaire.
    submit = SubmitField('Débannir')


# Formulaire permettant la création d'une nouvelle catégorie d'article.
class NewCategorieForm(FlaskForm):
    """
    Formulaire pour ajouter une nouvelle catégorie d'article.

    Attributes:
        nom (StringField) : Champ pour le nom de la catégorie.

    Example :
        form = NewCategorieForm()
    """
    nom = StringField("Nom de la catégorie", validators=[DataRequired()],
                      render_kw={'placeholder': "Saisir la nouvelle catégorie"})
    # Action de soumettre le formulaire.
    submit = SubmitField("Ajouter une catégorie")
    csrf_token = HiddenField()


# Formulaire permettant la création d'un nouveau sujet sur le forum.
class NewSubjectForumForm(FlaskForm):
    """
    Formulaire pour ajouter un nouveau sujet sur le forum.

    Attributes:
        nom (StringField) : Champ pour le nom du sujet pour le forum.

    Example :
        form = NewSubjectForumForm()
    """
    # Nom du sujet.
    nom = StringField("Nom du sujet", validators=[DataRequired()],
                      render_kw={'placeholder': "Veuillez entrer le nouveau sujet"})

    # Action de soumettre le formulaire.
    submit = SubmitField("Ajouter le sujet")
    csrf_token = HiddenField()


# Formulaire permettant la création d'un nouvel article.
class ArticleForm(FlaskForm):
    """
    Formulaire pour ajouter un nouvel article.

    Attributes:
        title (StringField) : Champ pour le titre de l'article.
        pseudo_author (StringField) : Champ pour le pseudo de l'auteur de l'article.
        article_content (TextAreaField) : Champ pour le contenu de l'article.
        resume (StringField) : Champ pour le résumé de l'article.
        date_edition (StringField) : Champ pour la date d'édition de l'article.

    Example:
        form = ArticleForm()
    """

    # Titre de l'article.
    title = StringField("Titre de l'article", validators=[DataRequired()],
                        render_kw={"placeholder": "Veuillez renseigner le titre de l'article."})

    # Pseudo de l'auteur.
    pseudo_author = StringField("Pseudo de l'auteur", validators=[DataRequired()],
                                render_kw={
                                    "placeholder": "Veuillez renseigner le pseudo de l'auteur de l'article."})

    # Contenu de l'article (champ TextAreaField pour permettre un contenu plus long).
    article_content = TextAreaField("Contenu de l'article", validators=[DataRequired()],
                                    render_kw={"placeholder": "Vous pouvez écrire votre article."})

    # Résumé de l'article.
    resume = StringField("Résumé de l'article", validators=[DataRequired()],
                         render_kw={"placeholder": "Veuillez écrire le résumé de l'article."})

    # Date d'édition de l'article.
    date_edition = StringField("Date d'édition", validators=[DataRequired()])

    # Action de soumettre le formulaire.
    submit = SubmitField("Ajouter l'article")


# Formulaire permettant à un utilisateur de créer un commentaire pour la section article.
class CommentArticleForm(FlaskForm):
    """
    Formulaire pour ajouter un commentaire à un article.

    Attributes :
        comment_content (TextAreaField) : Champ pour le contenu du commentaire.
        user_pseudo (StringField) : Champ pour le pseudo de l'utilisateur.

    Example :
        form = CommentArticleForm()
    """

    # Le contenu du commentaire.
    comment_content = TextAreaField("Contenu du commentaire", validators=[DataRequired()],
                                    render_kw={"placeholder": "Veuillez entrer votre commentaire."})

    # Le pseudo de l'utilisateur.
    user_pseudo = StringField("Pseudo de l'utilisateur", validators=[DataRequired()],
                              render_kw={"placeholder": "Veuillez renseigner votre pseudo."})

    # Action de soumettre le formulaire.
    submit = SubmitField("Soumettre le commentaire")

    csrf_token = HiddenField()


# Formulaire permettant à un utilisateur de créer un commentaire pour la section forum.
class CommentSubjectForm(FlaskForm):
    """
    Formulaire pour ajouter un commentaire à un sujet du forum.

    Attributes :
        comment_content (TextAreaField) : Champ pour le contenu du commentaire.
        user_pseudo (StringField) : Champ pour le pseudo de l'utilisateur.

    Example :
        form = CommentSubjectForm()
    """

    # Le contenu du commentaire.
    comment_content = TextAreaField("Contenu du commentaire", validators=[DataRequired()],
                                    render_kw={"placeholder": "Veuillez entrer votre commentaire."})

    # Le pseudo de l'utilisateur.
    user_pseudo = StringField("Pseudo de l'utilisateur", validators=[DataRequired()],
                              render_kw={"placeholder": "Veuillez renseigner votre pseudo."})

    # Action de soumettre le formulaire.
    submit = SubmitField("Soumettre le commentaire")

    csrf_token = HiddenField()


# Formulaire permettant de liker un article.
class LikeForm(FlaskForm):
    """
    Formulaire permettant de liker un article ou un commentaire.

    Example:
        form = LikeForm()
    """
    csrf_token = HiddenField()
    # Action de soumettre le formulaire.
    submit = SubmitField('👍')


# Formulaire permettant de disliker un article
class DislikeForm(FlaskForm):
    """
    Formulaire permettant de disliker un article ou un commentaire.

    Example:
        form = DislikeForm()
    """
    csrf_token = HiddenField()
    # Action de soumettre le formulaire.
    submit = SubmitField('👎')


# Formulaire permettant de liker un commentaire dans la section article.
class CommentLike(FlaskForm):
    """
    Formulaire permettant de liker un commentaire.

    Example:
        form = CommentLike()
    """
    csrf_token = HiddenField()
    submit = SubmitField()


# Formulaire permettant de répondre à un commentaire dans la section article.
class ReplyArticleForm(FlaskForm):
    """
    Formulaire permettant d'ajouter une réponse à un commentaire dans la section article.

    Attributes :
        reply_content (TextAreaField) : Champ de texte pour la réponse au commentaire.
        submit (SubmitField): Bouton de soumission du formulaire.
        csrf_token (HiddenField) : Jeton CSRF pour la sécurité du formulaire.
    """
    csrf_token = HiddenField()

    # Le contenu de la réponse.
    reply_content = TextAreaField("Réponse au commentaire", validators=[DataRequired()],
                                  render_kw={"placeholder": "Veuillez écrire votre commentaire."})

    # Action de soumettre le formulaire.
    submit = SubmitField()


# Formulaire permettant de répondre à un commentaire dans la section forum.
class ReplySubjectForm(FlaskForm):
    """
    Formulaire permettant d'ajouter une réponse à un commentaire dans la section forum.

    Attributes :
        reply_content (TextAreaField) : Champ de texte pour la réponse au commentaire.
        comment_id (HiddenField) : Champ caché pour l'ID du commentaire parent.
        submit (SubmitField): Bouton de soumission du formulaire.
        csrf_token (HiddenField) : Jeton CSRF pour la sécurité du formulaire.
    """
    csrf_token = HiddenField()
    # Le contenu de la réponse.
    reply_content = TextAreaField("Réponse au sujet du forum", validators=[DataRequired()],
                                  render_kw={"placeholder": "Veuillez écrire votre commentaire."})
    # Champ pour stocker l'id du commentaire parent.
    comment_id = HiddenField('ID du commentaire')
    # Action de soumettre le formulaire.
    submit = SubmitField()


# Formulaire permettant de filtrer les articles par catégorie.
class FilterForm(FlaskForm):
    """
    Formulaire permettant de filtrer les articles par catégories.

    Attributes :
        category (SelectField) : Champ de sélection pour choisir la catégorie.
        submit (SubmitField) : Bouton de soumission du formulaire.
    """
    category = SelectField('Categorie', choices=[])
    submit = SubmitField()


# Formulaire permettant de supprimer les commentaires dans la section forum.
class SuppressCommentSubjectForm(FlaskForm):
    """
    Formulaire pour supprimer un commentaire de la section forum.

    Attributes :
        comment_id (HiddenField) : Champ caché pour l'ID du commentaire à supprimer.
        submit (SubmitField): Bouton de soumission du formulaire.
    """
    comment_id = HiddenField('Comment_id', validators=[DataRequired()])
    submit = SubmitField('Supprimer')


# Formulaire permettant d'enregistrer une nouvelle biographie.
class CreateMangakaForm(FlaskForm):
    """
    Formulaire pour créer une biographie de mangaka.

    Attributes :
        mangaka_name (StringField) : Champ de texte pour le nom du mangaka.
        biography_content (TextAreaField) : Champ de texte pour le contenu de la biographie.
        date_bio_mangaka (StringField) : Champ de texte pour la date d'édition de la biographie.
        pseudo_author (StringField) : Champ de texte pour le pseudo de l'auteur de la biographie.
        submit (SubmitField): Bouton de soumission du formulaire.
        csrf_token (HiddenField) : Jeton CSRF pour la sécurité du formulaire.
    """
    # Nom du mangaka.
    mangaka_name = StringField(validators=[DataRequired()],
                               render_kw={"placeholder": "Veuillez renseigner le nom du mangaka."})
    # Contenu de la biographie.
    biography_content = TextAreaField('', validators=[DataRequired()],
                                      render_kw={"placeholder": "Veuillez saisir la biographie"})
    # Date d'édition de la biographie.
    date_bio_mangaka = StringField("Date d'édition", validators=[DataRequired()])

    # Pseudo de l'auteur.
    pseudo_author = StringField("Pseudo de l'auteur", validators=[DataRequired()],
                                render_kw={
                                    "placeholder": "Veuillez renseigner le pseudo de l'auteur de la biographie."})

    # Action de soumettre le formulaire.
    submit = SubmitField("Soumettre le commentaire")

    csrf_token = HiddenField()


# Formulaire permettant de laisser un commentaire dans la section biographie.
class CommentBiographyForm(FlaskForm):
    """
    Formulaire pour ajouter un commentaire à une biographie.

    Attributes :
        comment_content (TextAreaField) : Champ de texte pour le contenu du commentaire.
        user_pseudo (StringField) : Champ de texte pour le pseudo de l'utilisateur.
        submit (SubmitField): Bouton de soumission du formulaire.
        csrf_token (HiddenField) : Jeton CSRF pour la sécurité du formulaire.
    """

    # Le contenu du commentaire.
    comment_content = TextAreaField("Contenu du commentaire", validators=[DataRequired()],
                                    render_kw={"placeholder": "Veuillez entrer votre commentaire."})

    # Le pseudo de l'utilisateur.
    user_pseudo = StringField("Pseudo de l'utilisateur", validators=[DataRequired()],
                              render_kw={"placeholder": "Veuillez renseigner votre pseudo."})

    # Action de soumettre le formulaire.
    submit = SubmitField("Soumettre le commentaire")

    csrf_token = HiddenField()


# Formulaire permettant de liker une biographie.
class LikeBiographyForm(FlaskForm):
    """
    Formulaire permettant d'ajouter un like à une biographie.

    Attributes :
        csrf_token (HiddenField) : Jeton CSRF pour la sécurité du formulaire.
        submit (SubmitField): Bouton de soumission du formulaire (like).
    """
    csrf_token = HiddenField()
    # Action de soumettre le formulaire.
    submit = SubmitField('👍')


# Formulaire permettant de disliker une biographie.
class DislikeBiographyForm(FlaskForm):
    """
    Formulaire permettant d'ajouter un dislike à une biographie.

    Attributes :
        csrf_token (HiddenField) : Jeton CSRF pour la sécurité du formulaire.
        submit (SubmitField): Bouton de soumission du formulaire (dislike).
    """
    csrf_token = HiddenField()
    # Action de soumettre le formulaire.
    submit = SubmitField('👎')


# Formulaire permettant de disliker une biographie.
class CommentBiographyLike(FlaskForm):
    """
    Formulaire permettant de liker un commentaire dans la section biographie.

    Attributes :
        csrf_token (HiddenField) : Jeton CSRF pour la sécurité du formulaire.
        submit (SubmitField): Bouton de soumission du formulaire.
    """
    csrf_token = HiddenField()
    # Action de soumettre le formulaire.
    submit = SubmitField()


# Formulaire permettant de laisser une réponse à un commentaire dans la section biographie.
class ReplyBiographyForm(FlaskForm):
    """
    Formulaire permettant d'ajouter une réponse à un commentaire dans la section biographie.

    Attributes :
        reply_content (TextAreaField) : Champ de texte pour la réponse au commentaire.
        submit (SubmitField): Bouton de soumission du formulaire.
        csrf_token (HiddenField) : Jeton CSRF pour la sécurité du formulaire.
    """
    csrf_token = HiddenField()

    # Le contenu de la réponse.
    reply_content = TextAreaField("Réponse au commentaire", validators=[DataRequired()],
                                  render_kw={"placeholder": "Veuillez écrire votre commentaire."})

    # Action de soumettre le formulaire.
    submit = SubmitField()


# Formulaire permettant de supprimer un commentaire dans la section biographie.
class SuppressCommentBiographyForm(FlaskForm):
    """
    Formulaire pour supprimer un commentaire de la section biographie.

    Attributes :
        comment_id (HiddenField) : Champ caché pour l'ID du commentaire à supprimer.
        submit (SubmitField): Bouton de soumission du formulaire pour supprimer le commentaire.
    """
    comment_id = HiddenField('Comment_id', validators=[DataRequired()])
    submit = SubmitField('Supprimer')


# Formulaire permettant de supprimer une biographie.
class DeleteBiographyForm(FlaskForm):
    """
    Formulaire permettant de supprimer une biographie.

    Attributes :
        csrf_token (HiddenField) : Jeton CSRF pour la sécurité du formulaire.
    """
    csrf_token = HiddenField()


# Formulaire pour mot de passe oublié.
class ForgetPassword(FlaskForm):
    """
    Formulaire permettant de réinitialiser le mot de passe.

    Attributes :
        email(EmailField) : Email de l'utilisateur voulant réinitialiser son mot de passe.
        new_password (PasswordField) : Nouveau mot de passe.
        csrf_token (HiddenFields) : Jeton CSRF pour la sécurité du formulaire.
    """
    email = EmailField(
        "Email",
        validators=[DataRequired()],
        render_kw={"placeholder": "Entrez votre email"})
    new_password = PasswordField(
        "Nouveau mot de passe utilisateur",
        validators=[DataRequired()],
        render_kw={"placeholder": "Veuiller renseigner votre nouveau mot de passe Utilisateur."})
    new_password2 = PasswordField(
        "Confirmer le nouveau mot de passe",
        validators=[DataRequired(), EqualTo('password', message='Les mots de passe doivent correspondre.')],
        render_kw={"placeholder": "Veuillez confirmer votre nouveau mot de passe utilisateur."})
    csrf_token = HiddenField()

