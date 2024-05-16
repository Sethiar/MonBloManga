"""
Fichier de configuration pour les tests.
"""

import pytest
from create_app import create_app

@pytest.fixture
def app():
    """

    """
    app, _, _ = create_app()
    app.config.update({
        "TESTING": True,
    })

    with app.app_context():
        yield app