"""
Ceci est le code pour la configuration de l'application de mon blog
"""


# Modèle de la classe Config.
class Config:
    """
    Configuration de base de l'application.

    Cette classe définit les paramètres de configuration de base
    pour l'application Flask.
    """
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = True

    # Configuration de la base de données.
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Monolithe8@localhost:5432/db_monblogmanga"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Configuration de l'environnement de production.
class ProductConfig(Config):
    """
    Configuration de l'environnement de production.

    Cette classe étend la configuration de base (Config) et ajuste les
    paramètres spécifiques à l'environnement de production.
    """
    DEBUG = False


# Configuration de l'environnement de staging.
class StagingConfig(Config):
    """
    Configuration de l'environnement de staging.

    Cette classe étend la configuration de base (Config) et ajuste les
    paramètres spécifiques à l'environnement de staging.
    """
    DEVELOPMENT = True
    DEBUG = True


# Configuration de l'environnement de développement.
class DevelopmentConfig(Config):
    """
    Configuration de l'environnement de développement.

    Cette classe étend la configuration de base (Config) et ajuste les
    paramètres spécifiques à l'environnement de développement.
    """
    DEVELOPMENT = True
    DEBUG = True


# Configuration de l'environnement de test.
class TestingConfig(Config):
    """
    Configuration de l'environnement de test.

    Cette classe étend la configuration de base (Config) et ajuste les
    paramètres spécifiques à l'environnement de test.
    """
    TESTING = True
    WTF_CRSF_ENABLED = False
