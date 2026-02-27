
import { useState } from "react";
import { api } from "../api";

export default function ReviewForm({ productId, onAdded }) {

  // State qui contient le texte de l’avis
  const [text, setText] = useState("");

  // State pour la note 
  const [rating, setRating] = useState(5);

  // State pour afficher une information positive 
  const [info, setInfo] = useState("");

  // State pour gérer les erreurs éventuelles
  const [error, setError] = useState("");

  /*
    Fonction exécutée lors de la soumission du formulaire.
    Elle envoie l'avis au backend.
    Le backend analyse ensuite automatiquement le sentiment via l’IA.
  */
  async function submit(e) {
    e.preventDefault(); // Empêche le rechargement de la page
    setError(""); // Réinitialise les messages
    setInfo("");

    try {
      // Envoi d’une requête POST avec le texte et la note
      const { data } = await api.post(`/products/${productId}/reviews`, {
        text,
        rating: Number(rating), // Conversion en nombre (sécurité)
      });

      /*
        Le backend retourne :
        - sentiment (positif, négatif, neutre)
        - sentiment_score (score numérique)
        J’affiche le résultat directement à l’utilisateur.
      */
      setInfo(
        `Sentiment: ${data.sentiment} (score ${data.sentiment_score.toFixed(3)})`
      );

      // Réinitialisation du formulaire après succès
      setText("");
      setRating(5);

      // Si la fonction onAdded existe, je la déclenche
      // Cela permet au composant parent de recharger la liste des avis
      onAdded?.();

    } catch (err) {
      // Gestion des erreurs provenant du backend
      setError(err?.response?.data?.error || "Erreur");
    }
  }

  return (
    /*
      Formulaire stylisé avec Tailwind.
      L’IA est intégrée automatiquement côté backend,
      donc l’utilisateur n’a rien à configurer.
    */
    <form 
      onSubmit={submit} 
      className="rounded-2xl bg-white p-4 shadow-sm border space-y-3"
    >
      <h3 className="font-semibold">
        Ajouter un avis (IA auto)
      </h3>

      {/* Zone de texte pour saisir l’avis */}
      <textarea
        className="w-full rounded-xl border px-3 py-2 min-h-[90px]"
        placeholder="Texte de l’avis"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      {/* Sélection de la note */}
      <div className="flex items-center gap-3">
        <label className="text-sm text-gray-600">
          Note
        </label>

        <select
          className="rounded-xl border px-3 py-2"
          value={rating}
          onChange={(e) => setRating(e.target.value)}
        >
          {/* Génération dynamique des options 1 à 5 */}
          {[1,2,3,4,5].map((n) => (
            <option key={n} value={n}>
              {n}
            </option>
          ))}
        </select>
      </div>

      {/* Message d’information (résultat IA) */}
      {info && (
        <p className="text-sm text-green-700">
          {info}
        </p>
      )}

      {/* Message d’erreur si problème */}
      {error && (
        <p className="text-sm text-red-600">
          {error}
        </p>
      )}

      {/* Bouton d’envoi */}
      <button 
        className="rounded-xl bg-gray-900 px-4 py-2 text-white hover:bg-black"
      >
        Envoyer l’avis
      </button>
    </form>
  );
}