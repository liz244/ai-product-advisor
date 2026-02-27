# tests/test_stats_api.py
def test_stats_empty(client, product):
    res = client.get(f"/api/products/{product.id}/stats")
    assert res.status_code == 200

    data = res.get_json()
    assert data["total_reviews"] == 0
    assert data["avg_rating"] == 0.0
    assert data["sentiments"] == {"positive": 0, "neutral": 0, "negative": 0}


def test_stats_after_reviews(client, product, monkeypatch):
    import routes_reviews

    # 1) avis positif
    monkeypatch.setattr(routes_reviews, "analyze_sentiment", lambda text: {"sentiment": "positive", "score": 0.9})
    client.post(f"/api/products/{product.id}/reviews", json={"text": "Top", "rating": 5})

    # 2) avis négatif
    monkeypatch.setattr(routes_reviews, "analyze_sentiment", lambda text: {"sentiment": "negative", "score": 0.8})
    client.post(f"/api/products/{product.id}/reviews", json={"text": "Nul", "rating": 1})

    res = client.get(f"/api/products/{product.id}/stats")
    assert res.status_code == 200

    data = res.get_json()
    assert data["total_reviews"] == 2
    assert data["avg_rating"] == 3.0  # (5 + 1) / 2
    assert data["sentiments"]["positive"] == 1
    assert data["sentiments"]["negative"] == 1


def test_recommendations_endpoint_returns_expected_shape(client, product, monkeypatch):
    import routes_reviews

    # On mock build_recommendations pour éviter logique interne
    def fake_build_recommendations(negative_texts):
        return {
            "summary": "Résumé test",
            "weak_points": ["batterie"],
            "actions": ["Améliorer la batterie"],
        }

    monkeypatch.setattr(routes_reviews, "build_recommendations", fake_build_recommendations)

    # même sans avis négatif, endpoint doit renvoyer une structure JSON
    res = client.get(f"/api/products/{product.id}/recommendations")
    assert res.status_code == 200

    data = res.get_json()
    assert "summary" in data
    assert "weak_points" in data
    assert "actions" in data
    assert isinstance(data["actions"], list)