
from flask import Flask

# autoriser les requêtes cross-origin
from flask_cors import CORS
#  variables d’environnement .env
from dotenv import load_dotenv
#  configuration personnalisée
from config import Config
#  SQLAlchemy 
from extensions import db

# Import des blueprints 
from routes_products import bp_products
from routes_reviews import bp_reviews


def create_app():
    load_dotenv()
    app = Flask(__name__)
    # Chargement  depuis la classe Config
    app.config.from_object(Config)
    # Configuration du CORS :
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialisation de la base de données avec l'application
    db.init_app(app)

    # Création automatique des tables si elles n’existent pas
    with app.app_context():
        db.create_all()

    # Enregistrement des blueprints
   
    app.register_blueprint(bp_products)
    app.register_blueprint(bp_reviews)

    # Route simple pour vérifier que l’API fonctionne
    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app


# Point d’entrée de l’application


app = create_app()
if __name__ == "__main__":
    app.run(debug=True, port=5000)