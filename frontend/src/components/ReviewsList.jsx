import { useEffect, useState } from "react";
import { api } from "../api";

function badge(sentiment) {
  if (sentiment === "positive") return "bg-green-100 text-green-800";
  if (sentiment === "negative") return "bg-red-100 text-red-800";
  return "bg-yellow-100 text-gray-800";
}

export default function ReviewsList({ productId }) {
  const [reviews, setReviews] = useState([]);

  async function load() {
    const { data } = await api.get(`/products/${productId}/reviews`);
    setReviews(data);
  }

  useEffect(() => {
    load();
  }, [productId]);

  return (
    <div className="rounded-2xl bg-white p-4 shadow-sm border">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold">Avis</h3>
        <button onClick={load} className="text-sm text-gray-600 hover:underline">Rafraîchir</button>
      </div>

      <div className="mt-3 space-y-3">
        {reviews.map((r) => (
          <div key={r.id} className="rounded-xl border p-3">
            <div className="flex items-center justify-between gap-2">
              <div className="text-sm text-gray-600">Note: {r.rating}/5</div>
              <span className={`rounded-full px-2 py-1 text-xs ${badge(r.sentiment)}`}>
                {r.sentiment} • {Number(r.sentiment_score).toFixed(3)}
              </span>
            </div>
            <p className="mt-2">{r.text}</p>
            <p className="mt-2 text-xs text-gray-500">{new Date(r.created_at).toLocaleString()}</p>
          </div>
        ))}
        {reviews.length === 0 && <p className="text-sm text-gray-500">Aucun avis.</p>}
      </div>
    </div>
  );
}