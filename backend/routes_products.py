from flask import Blueprint, request, jsonify
from extensions import db
from models import Product

# Création du Blueprint pour isoler les routes liées aux produits
bp_products = Blueprint("bp_products", __name__)


# =========================================================
# GET - Récupérer tous les produits
# =========================================================
@bp_products.get("/api/products")
def get_products():
    """
    Retourne la liste complète des produits enregistrés.
    Les produits sont triés du plus récent au plus ancien.
    """
    products = Product.query.order_by(Product.id.desc()).all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "category": p.category
        }
        for p in products
    ])


# =========================================================
# POST - Créer un nouveau produit
# =========================================================
@bp_products.post("/api/products")
def create_product():
    """
    Crée un nouveau produit.
    Validation basique des champs obligatoires.
    """

    data = request.get_json() or {}

    name = (data.get("name") or "").strip()
    category = (data.get("category") or "").strip()

    if not name:
        return jsonify({"error": "Le nom est obligatoire"}), 400

    if not category:
        return jsonify({"error": "La catégorie est obligatoire"}), 400

    product = Product(
        name=name,
        category=category
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "id": product.id,
        "name": product.name,
        "category": product.category
    }), 201


# =========================================================
# DELETE - Supprimer un produit
# =========================================================
@bp_products.delete("/api/products/<int:product_id>")
def delete_product(product_id):
    """
    Supprime un produit existant.
    Retourne 404 si le produit n'existe pas.
    """

    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "Produit introuvable"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Produit supprimé avec succès"})