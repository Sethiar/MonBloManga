"""
Code permettant de définir les routes concernant les mécanismes d'authentification du blog.
"""

from app.auth import auth_bp

import bcrypt

from flask import session, redirect, url_for, request, current_app, render_template, flash
from flask_login import logout_user, login_user, login_required, current_user

from app.Models.forms import UserConnection
from app.Models.forms import AdminConnection

from app.Models.user import User
from app.Models.admin import Admin


# Route permettant à l'administrateur de joindre le formulaire de connexion.
@auth_bp.route("/connexion_admin_form", methods=['GET', 'POST'])
def admin_connection():
    """
    Route permettant d'accéder au formulaire de connexion pour l'administrateur.

    Returns:
        Template HTML du formulaire de connexion administrateur.

    Description:
        Cette route affiche un formulaire de connexion spécifiquement conçu pour l'administrateur
        du système. Le formulaire permet à l'administrateur de saisir ses identifiants
        (identifiant et mot de passe) afin d'accéder à son espace administrateur
        et de bénéficier de fonctionnalités réservées aux administrateurs.

    Example:
        L'administrateur accède à cette route via un navigateur web.
        La fonction renvoie le template HTML 'Admin/admin_connection.html' contenant le formulaire de connexion.
        L'administrateur saisit ses identifiants et soumet le formulaire pour se connecter à son espace administrateur.
    """
    # Création de l'instance du formulaire.
    form = AdminConnection()
    return render_template("Admin/admin_connection.html", form=form)


# Route permettant à l'admin de se déconnecter.
@auth_bp.route("/back_end_blog/admin_deconnexion", methods=['GET'])
def admin_logout():
    """
    Déconnecte l'administrateur actuellement authentifié.

    Cette fonction supprime les informations d'identification de l'administrateur de la session Flask.

    Returns:
        Redirige l'administrateur vers la page d'accueil après la déconnexion.
    """
    # Supprime les informations d'identification de l'utilisateur de la session.
    session.pop("logged_in", None)
    session.pop("identifiant", None)
    session.pop("admin_id", None)
    logout_user()

    # Redirige vers la page d'accueil après la déconnexion.
    return redirect(url_for('landing_page'))


# Route permettant à l'administrateur de se connecter.
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
                        f"L'administrateur {admin.identifiant} n'a pas le rôle de SuperAdmin, ses possibilités sont "
                        f"restreintes.")
            else:
                current_app.logger.warning(
                    f"Tentative de connexion échouée avec l'identifiant {identifiant}. Veuillez réessayer avec un "
                    f"autre identifiant.")
                return redirect(url_for("auth.admin_connection"))

    return render_template("Admin/admin_connection.html", form=form)


# Route permettant à l'utilisateur de joindre le formulaire de connexion.
@auth_bp.route("/connexion_utilisateur_formulaire", methods=['GET', 'POST'])
def user_connection():
    """
    Permet à l'utilisateur d'accéder au formulaire de connexion afin de s'identifier.

    Returns:
        Template HTML du formulaire d'authentification utilisateur.

    Description:
        Cette route affiche le formulaire permettant à l'utilisateur de saisir ses identifiants
        (pseudo et mot de passe) pour se connecter. Si l'utilisateur est déjà authentifié,
        il est redirigé vers la page d'accueil. Si l'utilisateur est banni, un message d'erreur
        est affiché et il est redirigé vers la page d'accueil.

    Example:
        L'utilisateur accède à cette route via un navigateur web.
        La fonction renvoie le template HTML 'User/user_connection.html' contenant le formulaire de connexion.
        L'utilisateur saisit ses identifiants et soumet le formulaire pour se connecter à son compte.
        En cas de succès, l'utilisateur est redirigé vers la page précédente ou la page d'accueil.
        En cas d'échec (par exemple, mauvais identifiants), l'utilisateur reste sur la même page avec un message d'erreur.
    """
    next_url = request.referrer
    print(next_url)
    session['next_url'] = next_url
    form = UserConnection()
    return render_template("User/user_connection.html", form=form, next_url=next_url)


# Route permettant à l'utilisateur de joindre le formulaire de connexion suite à une déconnexion.
@auth_bp.route("/connexion_utilisateur_formulaire_erreur", methods=['GET', 'POST'])
def user_connection_error():
    """
    Permet à l'utilisateur d'accéder au formulaire de connexion en cas d'erreur de connexion précédente.

    Returns:
        Template HTML du formulaire d'authentification utilisateur.

    Description:
        Cette route renvoie le formulaire d'authentification utilisateur pour permettre à l'utilisateur
        de se connecter à nouveau après une tentative de connexion infructueuse.

    Example:
        L'utilisateur accède à cette route via un navigateur web.
        La fonction renvoie le template HTML 'User/user_connection.html' contenant le formulaire de connexion.
        L'utilisateur peut saisir à nouveau ses identifiants pour se connecter.
    """
    form = UserConnection()
    return render_template("User/user_connection.html", form=form)


# Route permettant à l'utilisateur de se déconnecter.
@auth_bp.route("/deconnexion", methods=["GET"])
@login_required
def user_logout():
    """
    Déconnecte l'utilisateur actuellement authentifié.

    Cette fonction supprime les informations d'identification de l'utilisateur de la session Flask.

    Returns:
        Redirige l'utilisateur vers la page d'accueil après la déconnexion.
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
    Gère l'authentification de l'utilisateur.

    Cette fonction valide les informations de connexion de l'utilisateur et l'authentifie s'il réussit.

    Returns:
        Redirige l'utilisateur vers la page précédente ou la page d'accueil après une connexion réussie.

    Description:
        Cette route gère le processus d'authentification de l'utilisateur via le formulaire
        d'authentification 'UserConnection'. Si les informations de connexion sont valides,
        l'utilisateur est authentifié et ses informations sont stockées dans la session Flask.
        Ensuite, il est redirigé vers la page précédente s'il existe, sinon vers la page d'accueil.
        En cas d'échec d'authentification, l'utilisateur est redirigé vers la page de connexion avec un message d'erreur.
        De plus, si l'utilisateur est banni, il est empêché de se connecter et reçoit un message d'erreur approprié.

    Example:
        L'utilisateur accède à la route '/connexion_utilisateur' via un navigateur web.
        Il saisit ses informations d'identification (pseudo et mot de passe) dans le formulaire de connexion.
        Après soumission du formulaire, l'application vérifie les informations et authentifie l'utilisateur.
        Si l'authentification réussit, l'utilisateur est redirigé vers la page précédente ou la page d'accueil.
        Si l'utilisateur est banni, il reçoit un message d'erreur et ne peut pas se connecter.
        Sinon, en cas d'échec d'authentification, il est redirigé vers la page de connexion avec un message d'erreur.
    """
    # Récupère next_url depuis la session Flask
    next_url = session.get('next_url')

    # Création de l'instance du formulaire.
    form = UserConnection()

    if request.method == 'POST':
        if form.validate_on_submit():
            pseudo = form.pseudo.data
            password = form.password.data

            # Validation de la connexion.
            user = User.query.filter_by(pseudo=pseudo).first()
            if user is not None and bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
                if user.banned:
                    print("Votre compte a été banni. Vous ne pouvez pas vous connecter.")
                    return redirect(url_for('auth.user_banned', user_id=user.id))

                # Authentification réussie
                # Connexion de l'utilisateur et stockage de ses informations dans la session.
                login_user(user)
                session["logged_in"] = True
                session["pseudo"] = user.pseudo
                session["user_id"] = user.id
                current_app.logger.info(f"L'utilisateur {user.pseudo} s'est bien connecté.")

            if next_url:
                return redirect(next_url)
            else:
                return redirect(url_for('landing_page'))


        else:

            current_app.logger.warning(f"Tentative de connexion échouée avec l'utilisateur {form.pseudo.data}.")

            flash("Identifiant ou mot de passe incorrect. Veuillez réessayer.", "error")

            return redirect(url_for("auth.user_connection_error"))

    return render_template("User/user_connection.html", form=form)


# Route permettant de renseigner l'utilisateur qu'il a été banni.
@auth_bp.route("/utilisateur_banni,<int:user_id>", methods=['GET', 'POST'])
def user_banned(user_id):
    """
    Route pour informer l'utilisateur qu'il a été banni.

    :param user_id: ID de l'utilisateur
    :return: Template de l'utilisateur banni
    """
    # Récupération de l'id de l'utilisateur.
    user = User.query.get(user_id)
    if user is None:
        return "Utilisateur non trouvé", 404
        # Formater les dates sans les secondes et microsecondes.
    date_ban_end = user.date_ban_end.strftime("%Y-%m-%d %H:%M")
    date_banned = user.date_banned.strftime("%Y-%m-%d %H:%M")

    return render_template("Functional/user_banned.html", user=user, date_ban_end=date_ban_end, date_banned=date_banned)

