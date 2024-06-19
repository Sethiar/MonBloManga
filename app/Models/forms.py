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

    :param identifiant: Identifiant de l'administrateur.
    :param password: Mot de passe de l'administrateur.
    :param submit: Bouton de soumission du formulaire.

    Exemple :
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
        Formulaire de souscription pour les utilisateurs du site.

        :param email: Adresse e-mail de l'utilisateur.
        :param pseudo: Pseudo unique de l'utilisateur.
        :param password: Mot de passe de l'utilisateur.
        :param password2: Vérification de la concordance avec le premier mot de passe donné.
        :param profil_photo: Photo de l'utilisateur.
        :param date_naissance: Date de naissance de l'utilisateur.
        :param submit: Bouton de soumission du formulaire.

        Exemple :
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

    def validate_pseudo(self, pseudo):
        """
         Cette fonction permet de valider le fait que le pseudo utilisé n'existe pas dans la base de données.
        :param pseudo:
        """
        user = User.query.filter_by(pseudo=pseudo.data).first()
        if user:
            raise ValidationError('Ce pseudo est déjà utilisé. Veuillez en choisir un autre.')

    def validate_email(self, email):
        """
        Cette fonction permet de valider le fait que l'email n'existe pas dans la base de données.
        :param email:
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

    :param nom: Nom de l'auteur.
    :param prenom: Prénom de l'auteur.
    :param pseudo de l'auteur.
    :param submit: Bouton de soumission du formulaire.
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

    :param pseudo: Pseudo de l'utilisateur.
    :param password: Mot de passe de l'utilisateur.
    :param submit: Bouton de soumission du formulaire.

    Exemple :
        form = UserConnection()
    """
    pseudo = StringField("Pseudo", validators=[DataRequired()],
                         render_kw={"placeholder": "Veuillez renseigner votre pseudo."})
    password = PasswordField("Mot de passe", validators=[DataRequired()],
                             render_kw={"placeholder": "Veuillez renseigner votre mot de passe."})
    csrf_token = HiddenField()
    # Action de soumettre le formulaire.
    submit = SubmitField("se connecter")


# Formulaire permettant la création d'une nouvelle catégorie d'article.
class NewCategorieForm(FlaskForm):
    """
    Formulaire pour ajouter une nouvelle catégorie.

    :param nom: Nom de la catégorie.

    Exemple :
        form=NouvelleCategorieForm()
    """
    nom = StringField("Nom de la catégorie", validators=[DataRequired()],
                      render_kw={'placeholder': "Saisir la nouvelle catégorie"})
    # Action de soumettre le formulaire.
    submit = SubmitField("Ajouter une catégorie")
    csrf_token = HiddenField()


# Formulaire permettant la création d'un nouveau sujet sur le forum.
class NewSubjectForumForm(FlaskForm):
    """
    Formulaire pour ajouter un nouveau sujet pour le forum.

    :param nom: Nom du sujet pour le forum.

    Exemple :
        form=NewSubjectForumForm()
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
    Formulaire pour ajouter un article.

    :param titre: Titre de l'article.
    :param pseudo_auteur: Pseudo de l'auteur.
    :param contenu_article: Le contenu max 1000 caractères.
    :param date_edition: La date d'édition de l'article.

    Exemple :
        from=ArticleForm()
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
    Formulaire pour ajouter un commentaire à un article.
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
    Formulaire permettant d'ajouter un like à un article ou à un commentaire.
    """
    csrf_token = HiddenField()
    # Action de soumettre le formulaire.
    submit = SubmitField('👍')


# Formulaire permettant de disliker un article
class DislikeForm(FlaskForm):
    """
    Formulaire permettant d'ajouter un dislike à un article ou à un commentaire.
    """
    csrf_token = HiddenField()
    # Action de soumettre le formulaire.
    submit = SubmitField('👎')


# Formulaire permettant de liker un commentaire dans la section article.
class CommentLike(FlaskForm):
    csrf_token = HiddenField()
    submit = SubmitField()


# Formulaire permettant de répondre à un commentaire dans la section article.
class ReplyArticleForm(FlaskForm):
    """
    Formulaire permettant d'ajouter une réponse à un commentaire.
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
    Formulaire permettant d'ajouter une réponse à un commentaire dans la section du forum.
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
    """
    category = SelectField('Categorie', choices=[])
    submit = SubmitField()


# Formulaire permettant de supprimer les commentaires dans la section forum.
class SuppressCommentSubjectForm(FlaskForm):
    """
    Formulaire pour supprimer un commentaire de la section forum.
    """
    comment_id = HiddenField('Comment_id', validators=[DataRequired()])
    submit = SubmitField('Supprimer')


# Formulaire permettant d'enregistrer une nouvelle biographie.
class CreateMangakaForm(FlaskForm):
    """
    Formulaire pour créer une biographie de mangaka.
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
    Formulaire permettant d'ajouter un like à un article ou à un commentaire.
    """
    csrf_token = HiddenField()
    # Action de soumettre le formulaire.
    submit = SubmitField('👍')


# Formulaire permettant de disliker une biographie.
class DislikeBiographyForm(FlaskForm):
    """
    Formulaire permettant d'ajouter un dislike à une biographie ou à un commentaire.
    """
    csrf_token = HiddenField()
    # Action de soumettre le formulaire.
    submit = SubmitField('👎')


# Formulaire permettant de disliker une biographie.
class CommentBiographyLike(FlaskForm):

    csrf_token = HiddenField()
    # Action de soumettre le formulaire.
    submit = SubmitField()


# Formulaire permettant de laisser une réponse à un commentaire dans la section biographie.
class ReplyBiographyForm(FlaskForm):
    """
    Formulaire permettant d'ajouter une réponse à un commentaire.
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
    """
    comment_id = HiddenField('Comment_id', validators=[DataRequired()])
    submit = SubmitField('Supprimer')


# Formulaire permettant de supprimer une biographie.
class DeleteBiographyForm(FlaskForm):
    csrf_token = HiddenField()
