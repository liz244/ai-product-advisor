# Import du framework Flask pour créer l'application web
from flask import Flask

# Extension permettant d'autoriser les requêtes cross-origin
# (nécessaire pour que le frontend React puisse communiquer avec l'API)
from flask_cors import CORS

# Permet de charger les variables d’environnement (.env)
from dotenv import load_dotenv

# Import de la configuration personnalisée
from config import Config

# Import de l'instance SQLAlchemy (gestion base de données)
from extensions import db

# Import des blueprints (séparation des routes par modules)
from routes_products import bp_products
from routes_reviews import bp_reviews


def create_app():
    """
    Factory function qui crée et configure l'application Flask.
    Cette structure est recommandée pour les projets modulaires.
    """

    # Chargement des variables d’environnement
    load_dotenv()

    # Création de l’application Flask
    app = Flask(__name__)

    # Chargement des paramètres depuis la classe Config
    app.config.from_object(Config)

    # Configuration du CORS :
    # Autorise les requêtes venant du frontend (React)
    # uniquement sur les routes commençant par /api/*
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialisation de la base de données avec l'application
    db.init_app(app)

    # Création automatique des tables si elles n’existent pas
    with app.app_context():
        db.create_all()

    # Enregistrement des blueprints
    # Cela permet d’organiser les routes par fonctionnalité
    app.register_blueprint(bp_products)
    app.register_blueprint(bp_reviews)

    # Route simple pour vérifier que l’API fonctionne
    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app


# Point d’entrée de l’application
if __name__ == "__main__":
    app = create_app()

    # Lancement du serveur en mode debug (développement)
    app.run(debug=True, port=5000)