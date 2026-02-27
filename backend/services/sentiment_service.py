import os
from transformers import pipeline

# Chargement 1 seule fois au démarrage
_MODEL_NAME = os.getenv("HF_MODEL", "cardiffnlp/twitter-roberta-base-sentiment-latest")
_sentiment_pipe = pipeline("sentiment-analysis", model=_MODEL_NAME)

LABEL_MAP = {
    "positive": "positive",
    "neutral": "neutral",
    "negative": "negative",
    "LABEL_2": "positive",  # fallback (selon modèles)
    "LABEL_1": "neutral",
    "LABEL_0": "negative",
}

def analyze_sentiment(text: str) -> dict:
    """
    Returns: {sentiment: 'positive|neutral|negative', score: float}
    """
    result = _sentiment_pipe(text[:512])[0]
    label = result.get("label", "").lower()
    score = float(result.get("score", 0.0))

    sentiment = LABEL_MAP.get(label, label)
    if sentiment not in ("positive", "neutral", "negative"):
        # dernier filet de sécurité
        sentiment = "neutral"

    return {"sentiment": sentiment, "score": score}