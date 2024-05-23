"""

"""

import bcrypt

from flask import session, redirect, url_for, request, current_app, render_template
from flask_login import logout_user, login_user, login_required

from Models.forms import UserConnection
from Models.forms import AdminConnection

from Models.user import User
from Models.admin import Admin
from app.auth import auth_bp


@auth_bp.route("/connexion_admin_form", methods=['GET', 'POST'])
def admin_connection():
    """
    Route permettant d'accéder au formulaire de connexion pour l'administrateur.

    Returns:
        Template HTML du formulaire de connexion administrateur.

    Description:
        Cette route affiche un formulaire de connexion spécifiquement conçu pour l'administrateur
        du système. Le formulaire permet à l'administrateur de saisir ses identifiants
        (nom d'utilisateur et mot de passe) afin d'accéder à son espace administrateur
        et de bénéficier de fonctionnalités réservées aux administrateurs.

    Example:
        L'administrateur accède à cette route via un navigateur web.
        La fonction renvoie le template HTML 'Admin/admin_connection.html' contenant le formulaire de connexion.
        L'administrateur saisit ses identifiants et soumet le formulaire pour se connecter à son espace administrateur.
    """
    # Création de l'instance du formulaire.
    form = AdminConnection()
    return render_template("Admin/admin_connection.html", form=form)


@auth_bp.route("/back_end_blog/admin_deconnexion", methods=['GET'])
def admin_logout():
    """
    Déconnecte l'administrateur actuellement authentifié et l'admin du système.

    Cette fonction gère la déconnexion des administrateurs en supprimant les informations d'identification stockées dans la session Flask.

     Les sessions Flask sont un mécanisme permettant de stocker des données spécifiques à un utilisateur entre différentes requêtes HTTP.
     Dans ce cas, les informations d'identification telles que l'état de connexion, l'identifiant de l'utilisateur et l'identifiant de
     session sont stockées dans la session Flask lorsqu'un utilisateur se connecte avec succès. Cette fonction supprime ces informations de
     la session lorsqu'un utilisateur se déconnecte.

    Returns :
        redirige l'administrateur vers la page accueil.html après la déconnexion.

    Notes :
        La déconnexion est effectuée en supprimant les clés de session "logged_in", "identifiant" et "admin_id".
        Si aucun utilisateur n'est connecté, cette fonction n'a aucun effet et redirige simplement vers la page accueil.html.
    """
    # Supprime les informations d'identification de l'utilisateur de la session.
    session.pop("logged_in", None)
    session.pop("identifiant", None)
    session.pop("admin_id", None)
    logout_user()

    # Redirige vers la page d'accueil après la déconnexion.
    return redirect(url_for('landing_page'))


@auth_bp.route("/connexion_admin", methods=['GET', 'POST'])
def login_admin():
    """
    Gère l'authentification de l'administrateur pour accéder au back-end du blog.

    Cette route gère le processus d'authentification de l'administrateur afin de lui permettre d'accéder
    à l'interface back-end du blog. L'administrateur saisit son identifiant, son mot de passe et son rôle
    (par exemple, SuperAdmin) via un formulaire de connexion dédié.

    Returns:
        - Redirige l'administrateur vers la page back_end s'il est authentifié avec succès.
        - Redirige l'administrateur vers la page de connexion admin_connection si l'authentification échoue.

    Notes:
        - En cas de succès, les informations d'identification de l'administrateur sont stockées dans la session Flask
          pour maintenir sa connexion active.
        - En cas d'échec de l'authentification, l'administrateur est redirigé vers la page de connexion admin_connection
          avec un avertissement approprié.
        - Les journaux d'application sont utilisés pour enregistrer les tentatives de connexion réussies et les erreurs.

    Example:
        L'administrateur accède à la route '/connexion_admin' via un navigateur web.
        Il saisit ses informations d'identification (identifiant, mot de passe et rôle) dans le formulaire de connexion.
        Après soumission du formulaire, l'application vérifie les informations et authentifie l'administrateur.
        Si l'authentification réussit, l'administrateur est redirigé vers la page back_end du blog.
        Sinon, il est redirigé vers la page de connexion admin_connection avec un message d'erreur.
    """
    # Création de l'instance du formulaire.
    form = AdminConnection()

    if request.method == 'POST':
        if form.validate_on_submit():
            identifiant = form.identifiant.data
            password = form.password.data
            role = form.role.data

            # Validation de la connexion.
            admin = Admin.query.filter_by(identifiant=identifiant).first()
            if admin is not None and bcrypt.checkpw(password.encode('utf-8'), admin.password_hash):

                # Authentification réussie.
                if role == "SuperAdmin":
                    current_app.logger.info(f"L'administrateur {admin.identifiant} s'est bien connecté.")

                    # Connexion de l'admin et stockage de ses informations dans la session.
                    session["logged_in"] = True
                    session["identifiant"] = admin.identifiant
                    session["user_id"] = admin.id

                    return redirect(url_for("admin.back_end"))
                else:
                    current_app.logger.warning(
                        f"L'administrateur {admin.identifiant} n'a pas le rôle de SuperAdmin, ses possibilités sont restreintes.")
            else:
                current_app.logger.warning(
                    f"Tentative de connexion échouée avec l'identifiant {identifiant}. Veuillez réessayer avec un autre identifiant.")
                return redirect(url_for("auth.admin_connection"))

    return render_template("Admin/admin_connection.html", form=form)


@auth_bp.route("/connexion_utilisateur_formulaire", methods=['GET', 'POST'])
def user_connection():
    """
    Permet à l'utilisateur d'accéder au formulaire de connexion afin de s'identifier.

    Return :
        Redirige vers le formulaire d'authentification utilisateur.
    """
    next_url = request.referrer
    print(next_url)
    session['next_url'] = next_url
    form = UserConnection()
    return render_template("User/user_connection.html", form=form, next_url=next_url)


@auth_bp.route("/deconnexion", methods=["GET"])
@login_required
def user_logout():
    """
    Déconnecte l'utilisateur actuellement authentifié et l'admin du système.

    Cette fonction gère la déconnexion des utilisateurs en supprimant les informations d'identification stockées dans la session Flask.

     Les sessions Flask sont un mécanisme permettant de stocker des données spécifiques à un utilisateur entre différentes requêtes HTTP.
     Dans ce cas, les informations d'identification telles que l'état de connexion, l'identifiant de l'utilisateur et l'identifiant de
     session sont stockées dans la session Flask lorsqu'un utilisateur se connecte avec succès. Cette fonction supprime ces informations de
     la session lorsqu'un utilisateur se déconnecte.

    Returns :
        redirige l'utilisateur vers la page accueil.html après la déconnexion.

    Notes :
        La déconnexion est effectuée en supprimant les clés de session "logged_in", "identifiant" et "user_id".
        Si aucun utilisateur n'est connecté, cette fonction n'a aucun effet et redirige simplement vers la page accueil.html.
    """
    # Supprime les informations d'identification de l'utilisateur de la session.
    session.pop("logged_in", None)
    session.pop("identifiant", None)
    session.pop("user_id", None)
    logout_user()

    # Redirige vers la page d'accueil après la déconnexion.
    return redirect(url_for('landing_page'))


@auth_bp.route("/connexion_utilisateur", methods=['GET', 'POST'])
def login():
    """
    Gère l'authentification de l'utilisateur afin qu'il puisse laisser un commentaire ou
    ajouter un sujet sur le forum.
    Returns:
        Redirige l'utilisateur sur la page d'accueil avec son nom sur le fichier html.
    """
    # Récupère next_url depuis la session Flask
    next_url = session.get('next_url')
    print(next_url)

    # Création de l'instance du formulaire.
    form = UserConnection()

    if request.method == 'POST':
        if form.validate_on_submit():
            pseudo = form.pseudo.data
            password = form.password.data

            # Validation de la connexion.
            user = User.query.filter_by(pseudo=pseudo).first()
            login_user(user)
            if user is not None and bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
                # Authentification réussie
                current_app.logger.info(f"L'utilisateur {user.pseudo} s'est bien connecté.")
                # Connexion de l'utilisateur et stockage de ses informations dans la session.
                session["logged_in"] = True
                session["pseudo"] = user.pseudo
                session["user_id"] = user.id

            if next_url:
                return redirect(next_url)
            else:
                return redirect(url_for('landing_page'))

        else:
            current_app.logger.warning(
                f"Tentative de connexion échouée avec l'utilisateur {form.pseudo.data}.")
            return redirect(url_for("auth.user_connection"))


