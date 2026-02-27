AI Product Advisor

Application web fullstack permettant d’analyser automatiquement les avis clients d’un produit grâce à un modèle d’intelligence artificielle, d’en extraire des statistiques dynamiques et de générer des recommandations d’amélioration.

1. Présentation du projet

AI Product Advisor est une application web composée de :

Un front-end développé en React (Vite + Tailwind CSS)

Un back-end développé en Flask (Python)

Une base de données SQLite

Un module d’analyse de sentiment basé sur Hugging Face Transformers

L’application permet :

Créer un produit

Ajouter des avis clients

Analyser automatiquement le sentiment des avis

Calculer des statistiques dynamiques

Visualiser la distribution des sentiments (PieChart)

Générer des recommandations automatiques

2. Architecture du projet

Architecture fullstack séparée :

AI-Product-Advisor/
│
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── routes/
│   ├── services/
│   ├── database.db
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── api.js
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md

Le front communique avec le back via API REST en JSON.

3. Prérequis

Avant installation, vérifier :

Node.js (>= 18)

npm

Python (>= 3.9)

pip

4. Installation et lancement
4.1 Lancer le Back-end

Se placer dans le dossier backend :

cd backend

Créer un environnement virtuel :

python -m venv venv

Activer l’environnement :

Windows :

venv\Scripts\activate

Mac / Linux :

source venv/bin/activate

Installer les dépendances :

pip install -r requirements.txt

Lancer le serveur :

python app.py

Le serveur démarre sur :

http://127.0.0.1:5000
4.2 Lancer le Front-end

Dans un autre terminal :

cd frontend
npm install
npm run dev

Le front démarre sur :

http://localhost:5173
5. Base de données

Base utilisée : SQLite

Fichier : database.db

Structure relationnelle :

Table Products :

id (clé primaire)

name

category

created_at

Table Reviews :

id

product_id (clé étrangère)

text

rating

sentiment

sentiment_score

created_at

Relation :
Un produit possède plusieurs avis (1 → N).

La base est automatiquement initialisée au premier lancement.

6. Endpoints API REST
Produits

GET /products
→ Récupère tous les produits

POST /products
→ Crée un produit

DELETE /products/<id>
→ Supprime un produit

Avis

POST /products/<id>/reviews
→ Ajoute un avis avec analyse automatique

GET /products/<id>/reviews
→ Liste les avis d’un produit

Statistiques

GET /products/<id>/stats
→ Retourne :

total_reviews

avg_rating

distribution sentiments

Recommandations

GET /products/<id>/recommendations
→ Génère :

points faibles récurrents

recommandations d’amélioration

7. Modèle IA utilisé

Bibliothèque : Hugging Face Transformers

Modèle :
cardiffnlp/twitter-roberta-base-sentiment-latest

Fonctionnement :

Le texte de l’avis est envoyé au backend

Le modèle analyse le sentiment

Il retourne :

label (positive / neutral / negative)

score de confiance

Les résultats sont stockés en base

Limite :
Le modèle est principalement entraîné en anglais.

8. Gestion des erreurs

Le système gère :

Champs vides

Produit inexistant

Erreurs API

Erreurs base de données

Les réponses API utilisent des codes HTTP standards :

200 : OK

400 : erreur utilisateur

404 : ressource inexistante

500 : erreur serveur

9. Responsive Design

Le front est développé en mobile-first avec Tailwind CSS.

Breakpoints utilisés :

md

lg

Le layout s’adapte automatiquement sur :

Mobile

Tablette

Desktop

10. Sécurité

Utilisation d’un ORM (SQLAlchemy)

Pas d’accès direct à la base depuis le front

API REST contrôlée

Séparation front/back

Améliorations futures possibles :

Authentification JWT

Validation avancée

Rate limiting



