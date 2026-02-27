from datetime import datetime
from extensions import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    reviews = db.relationship("Review", backref="product", cascade="all, delete-orphan")

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1..5

    sentiment = db.Column(db.String(20), nullable=False)        # positive/neutral/negative
    sentiment_score = db.Column(db.Float, nullable=False)       # confidence

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)