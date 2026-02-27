import re
from collections import Counter

STOPWORDS_FR = {
    "le","la","les","un","une","des","de","du","et","à","a","au","aux","en","pour","par","sur","dans",
    "avec","sans","ce","cette","ces","mon","ma","mes","ton","ta","tes","son","sa","ses","leur","leurs",
    "je","tu","il","elle","on","nous","vous","ils","elles","mais","donc","or","ni","car",
    "est","sont","être","avoir","fait","très","trop","plus","moins","pas","ne","que","qui","quoi","dont",
}

# mapping mots-clés -> recommandations
RECO_MAP = [
    ({"batterie", "autonomie", "charge"}, "Améliorer l’autonomie / optimiser la consommation et la charge."),
    ({"livraison", "retard", "transport", "colis"}, "Renforcer la qualité logistique (délais, suivi, emballage)."),
    ({"qualité", "fragile", "cassé", "casse"}, "Travailler la qualité perçue (matériaux, contrôle qualité)."),
    ({"prix", "cher", "coût"}, "Revoir la stratégie prix / proposer des bundles ou promos ciblées."),
    ({"service", "support", "sav", "réponse"}, "Améliorer le support client (délais de réponse, FAQ, processus SAV)."),
    ({"son", "audio", "bruit", "grésillement"}, "Optimiser la performance audio (calibrage, réduction bruit, tests)."),
]

def _tokenize(text: str):
    text = text.lower()
    text = re.sub(r"[^a-zàâçéèêëîïôûùüÿñæœ0-9\s-]", " ", text)
    tokens = re.split(r"\s+", text)
    tokens = [t for t in tokens if len(t) >= 3 and t not in STOPWORDS_FR and not t.isdigit()]
    return tokens

def extract_top_terms(negative_texts, top_k=8):
    tokens = []
    for t in negative_texts:
        tokens.extend(_tokenize(t))
    counts = Counter(tokens)
    return [w for w, _ in counts.most_common(top_k)]

def build_recommendations(negative_texts):
    """
    Returns: {summary: str, weak_points: list[str], actions: list[str]}
    """
    if not negative_texts:
        return {
            "summary": "Aucun retour négatif significatif pour ce produit.",
            "weak_points": [],
            "actions": ["Continuer à surveiller les avis et maintenir la qualité."],
        }

    top_terms = extract_top_terms(negative_texts, top_k=10)

    # Weak points = top terms (filtrés) + mapping recos
    actions = []
    matched = set()
    for terms, action in RECO_MAP:
        if any(t in terms for t in top_terms):
            actions.append(action)
            matched.update(terms)

    # compléter si pas assez d’actions
    if len(actions) < 3:
        actions.append("Analyser plus finement les irritants (catégories, lots, versions produit).")
    if len(actions) < 4:
        actions.append("Mettre en place un suivi post-achat (questionnaire court + NPS).")
    if len(actions) < 5:
        actions.append("Ajouter des informations claires sur la fiche produit (usage, limites, entretien).")

    actions = actions[:5]

    summary = (
        "Les retours négatifs se concentrent principalement autour de : "
        + ", ".join(top_terms[:6])
        + "."
    )

    weak_points = top_terms[:8]
    return {"summary": summary, "weak_points": weak_points, "actions": actions}