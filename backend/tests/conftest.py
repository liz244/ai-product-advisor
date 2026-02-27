# tests/conftest.py
import sys
import os
import pytest

# Ajoute le dossier backend au path Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from extensions import db
from models import Product


@pytest.fixture()
def app():
    """
    Crée une application Flask en mode test avec une DB SQLite in-memory.
    """
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    """
    Client HTTP de test Flask.
    Permet de faire des GET/POST/DELETE comme le frontend.
    """
    return app.test_client()


@pytest.fixture()
def product(app):
    """
    Crée un produit en base pour pouvoir tester reviews/stats.
    """
    with app.app_context():
        p = Product(name="Produit Test", category="test")
        db.session.add(p)
        db.session.commit()
        return p