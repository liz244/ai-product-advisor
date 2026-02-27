from app import create_app
from extensions import db
from models import Product

app = create_app()

with app.app_context():
    if Product.query.count() == 0:
        db.session.add(Product(name="Casque Bluetooth ZX-1", category="audio"))
        db.session.add(Product(name="Tapis de Yoga Pro", category="sport"))
        db.session.add(Product(name="Aspirateur Compact CleanGo", category="maison"))
        db.session.commit()
        print("Seed OK")
    else:
        print("Seed déjà présent")