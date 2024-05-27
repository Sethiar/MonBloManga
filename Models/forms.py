"""Modèles des formulaires"""

from flask_wtf import FlaskForm
from flask import render_template
from wtforms import StringField, PasswordField, HiddenField, \
    EmailField, DateField, SubmitField, TextAreaField

from wtforms.validators import DataRequired, EqualTo, ValidationError
from Models.user import User


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


class UserSaving(FlaskForm):
    """
        Formulaire de souscription pour les utilisateurs du site.

        :param email: Adresse e-mail de l'utilisateur.
        :param pseudo: Pseudo unique de l'utilisateur.
        :param password: Mot de passe de l'utilisateur.
        :param password2: Vérification de la concordance avec le premier mot de passe donné.
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


class CommentForm(FlaskForm):
    """
    Formulaire pour ajouter un commentaire à un article.
    """

    # Le contenu du commentaire.
    comment_content = TextAreaField("Contenu du commentaire", validators=[DataRequired()],
                                    render_kw={"placeholder": "Veuillez entrer votre commentaire."})

    # Le pseudo de l'utilisateur.
    user_pseudo = StringField("Pseudo de l'utilisateur", validators=[DataRequired()],
                              render_kw={"placeholder": "Veuillez renseigner votre pseudo."})

    # La date du commentaire.
    comment_date = StringField("Date du commentaire", validators=[DataRequired()])

    # Action de soumettre le formulaire.
    submit = SubmitField()

    csrf_token = HiddenField()


class LikeForm(FlaskForm):
    """
    Formulaire permettant d'ajouter un like à un article ou à un commentaire.
    """
    csrf_token = HiddenField()
    # Action de soumettre le formulaire.
    submit = SubmitField('👍')


class DislikeForm(FlaskForm):
    """
    Formulaire permettant d'ajouter un dislike à un article ou à un commentaire.
    """
    csrf_token = HiddenField()
    # Action de soumettre le formulaire.
    submit = SubmitField('👎')


class ReplyForm(FlaskForm):
    """
    Formulaire permettant d'ajouter une réponse à un commentaire.
    """
    csrf_token = HiddenField()

    # Le contenu de la réponse.
    reply_content = TextAreaField("Réponse au commentaire", validators=[DataRequired()],
                                  render_kw={"placeholder": "Veuillez écrire votre commentaire."})

    # La date du commentaire.
    comment_date = DateField("Date du commentaire", validators=[DataRequired()])
    # Action de soumettre le formulaire.
    submit = SubmitField()
