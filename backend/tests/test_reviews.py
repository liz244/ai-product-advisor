# tests/test_reviews_api.py
def test_list_reviews_404(client):
    res = client.get("/api/products/9999/reviews")
    assert res.status_code == 404
    assert res.get_json()["error"] == "Produit introuvable"


def test_add_review_requires_text(client, product):
    res = client.post(
        f"/api/products/{product.id}/reviews",
        json={"text": "", "rating": 5},
    )
    assert res.status_code == 400
    assert "text est obligatoire" in res.get_json()["error"]


def test_add_review_requires_rating_int_1_to_5(client, product):
    # rating hors plage
    res = client.post(
        f"/api/products/{product.id}/reviews",
        json={"text": "Ok", "rating": 10},
    )
    assert res.status_code == 400

    # rating pas int
    res2 = client.post(
        f"/api/products/{product.id}/reviews",
        json={"text": "Ok", "rating": "5"},
    )
    assert res2.status_code == 400


def test_add_review_success_returns_sentiment_json(client, product, monkeypatch):
    """
    On mock l'IA pour éviter de charger le modèle Hugging Face dans les tests.
    """
    from routes_reviews import analyze_sentiment as real_analyze  # juste pour montrer le contexte
    import routes_reviews

    def fake_analyze_sentiment(text):
        return {"sentiment": "positive", "score": 0.987}

    monkeypatch.setattr(routes_reviews, "analyze_sentiment", fake_analyze_sentiment)

    res = client.post(
        f"/api/products/{product.id}/reviews",
        json={"text": "Très bon produit", "rating": 5},
    )
    assert res.status_code == 201

    data = res.get_json()
    assert "id" in data
    assert data["sentiment"] == "positive"
    assert abs(data["sentiment_score"] - 0.987) < 1e-9


def test_list_reviews_after_adding_one(client, product, monkeypatch):
    import routes_reviews

    monkeypatch.setattr(
        routes_reviews,
        "analyze_sentiment",
        lambda text: {"sentiment": "neutral", "score": 0.555},
    )

    # Add review
    post = client.post(
        f"/api/products/{product.id}/reviews",
        json={"text": "Bof", "rating": 3},
    )
    assert post.status_code == 201

    # List
    res = client.get(f"/api/products/{product.id}/reviews")
    assert res.status_code == 200

    arr = res.get_json()
    assert isinstance(arr, list)
    assert len(arr) == 1

    r = arr[0]
    assert r["product_id"] == product.id
    assert r["text"] == "Bof"
    assert r["rating"] == 3
    assert r["sentiment"] == "neutral"
    assert "created_at" in r