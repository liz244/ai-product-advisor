from flask import Blueprint, request, jsonify

# db = instance SQLAlchemy (session + connexion à la base)
from extensions import db

# Modèles ORM (tables Product et Review)
from models import Product, Review

# Services "métier" : IA sentiment + génération de recommandations
from services.sentiment_service import analyze_sentiment
from services.recommendation_service import build_recommendations

# Blueprint = module de routes séparé (meilleure organisation du backend)
# url_prefix="/api" : toutes les routes de ce fichier commencent par /api
bp_reviews = Blueprint("reviews", __name__, url_prefix="/api")


@bp_reviews.get("/products/<int:product_id>/reviews")
def list_reviews(product_id):
    """
    Retourne la liste des avis d’un produit (triés du plus récent au plus ancien).
    Cette route est utilisée par le frontend pour afficher ReviewsList.
    """

    # Vérifie que le produit existe avant de chercher ses avis
    p = Product.query.get(product_id)
    if not p:
        return jsonify({"error": "Produit introuvable"}), 404

    # Récupération des avis liés au produit + tri par date décroissante
    reviews = (
        Review.query
        .filter_by(product_id=product_id)
        .order_by(Review.created_at.desc())
        .all()
    )

    # Jerenvoie une liste JSON, pas les objets SQLAlchemy directement
    return jsonify([
        {  
            "id": r.id,
            "product_id": r.product_id,
            "text": r.text,
            "rating": r.rating,
            "sentiment": r.sentiment,
            "sentiment_score": r.sentiment_score,
            # isoformat() pour transmettre une date propre (format standard)
            "created_at": r.created_at.isoformat(),
        }
        for r in reviews
    ])


@bp_reviews.post("/products/<int:product_id>/reviews")
def add_review(product_id):
    """
    Ajoute un nouvel avis sur un produit.
    Particularité : le sentiment est calculé automatiquement par l’IA au moment de l’ajout.
    Cette route est utilisée par ReviewForm.
    """

    # Vérifie que le produit existe
    p = Product.query.get(product_id)
    if not p:
        return jsonify({"error": "Produit introuvable"}), 404

    # Récupère le JSON envoyé par le frontend
    data = request.get_json(force=True)

    # Nettoyage du texte (strip pour enlever espaces / retours)
    text = (data.get("text") or "").strip()

    # Récupère la note (doit être un entier entre 1 et 5)
    rating = data.get("rating")

    # Validation côté backend (important même si le frontend valide déjà)
    if not text:
        return jsonify({"error": "text est obligatoire"}), 400

    # Ici je force une validation stricte : int + plage 1..5
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({"error": "rating doit être un entier entre 1 et 5"}), 400

    # ===== IA : analyse automatique du sentiment =====
    # Le service retourne par exemple { "sentiment": "positive", "score": 0.93 }
    res = analyze_sentiment(text)

    # Création de l'avis avec les champs IA stockés en base
    r = Review(
        product_id=product_id,
        text=text,
        rating=rating,
        sentiment=res["sentiment"],
        sentiment_score=res["score"],
    )

    # Écriture en base de données
    db.session.add(r)
    db.session.commit()

    # Retour minimal utile au frontend (affichage immédiat du résultat IA)
    return jsonify({
        "id": r.id,
        "sentiment": r.sentiment,
        "sentiment_score": r.sentiment_score,
    }), 201


@bp_reviews.get("/products/<int:product_id>/stats")
def product_stats(product_id):
    """
    Retourne des statistiques agrégées pour un produit :
    - total d’avis
    - moyenne des notes
    - répartition des sentiments (positive/neutral/negative)
    Cette route est utilisée par StatsCard (graphique).
    """

    # Vérifie que le produit existe
    p = Product.query.get(product_id)
    if not p:
        return jsonify({"error": "Produit introuvable"}), 404

    # Récupération de tous les avis du produit
    reviews = Review.query.filter_by(product_id=product_id).all()

    # Calcul du total
    total = len(reviews)

    # Calcul de la moyenne (avec protection si total = 0)
    avg_rating = round(sum(r.rating for r in reviews) / total, 2) if total else 0.0

    # Comptage des sentiments (structure attendue par le frontend)
    sentiments = {"positive": 0, "neutral": 0, "negative": 0}
    for r in reviews:
        if r.sentiment in sentiments:
            sentiments[r.sentiment] += 1

    # Réponse JSON consommée directement par le frontend
    return jsonify({
        "total_reviews": total,
        "avg_rating": avg_rating,
        "sentiments": sentiments,
    })


@bp_reviews.get("/products/<int:product_id>/recommendations")
def product_recommendations(product_id):
    """
    Génère des recommandations à partir des avis négatifs.
    Principe : on filtre les avis négatifs, on récupère leurs textes,
    puis on appelle un service qui construit une synthèse + actions proposées.
    Cette route est utilisée par le composant Recommendations.
    """

    # Vérifie que le produit existe
    p = Product.query.get(product_id)
    if not p:
        return jsonify({"error": "Produit introuvable"}), 404

    # On récupère uniquement les avis négatifs (objectif : améliorer le produit)
    negative_reviews = Review.query.filter_by(
        product_id=product_id,
        sentiment="negative"
    ).all()

    # Extraction des textes pour les analyser côté service
    negative_texts = [r.text for r in negative_reviews]

    # Construction des recommandations (résumé + points faibles + actions)
    reco = build_recommendations(negative_texts)

    return jsonify(reco)