
import { useEffect, useState } from "react";
import { api } from "../api";
export default function Recommendations({ productId }) {

  // State qui va contenir les données de recommandation retournées par l'API
  const [data, setData] = useState(null);
  /*
    Fonction qui récupère les recommandations
    liées au produit sélectionné.
    Elle envoie une requête GET vers le backend.
  */
  async function load() {
    const res = await api.get(`/products/${productId}/recommendations`);
    setData(res.data); // Stockage des données reçues dans le state
  }

  /*
    useEffect est déclenché :
    - au premier rendu
    - à chaque fois que productId change

    Cela permet de recharger automatiquement
    les recommandations quand on change de produit.
  */
  useEffect(() => {
    load();
  }, [productId]);

  // Tant que les données ne sont pas encore chargées,
  // j'affiche un état de chargement.
  if (!data) {
    return (
      <div className="rounded-2xl bg-white p-4 shadow-sm border">
        Chargement reco…
      </div>
    );
  }

  return (
    <div className="rounded-2xl bg-white p-4 shadow-sm border">

      {/* Header avec bouton de rafraîchissement manuel */}
      <div className="flex items-center justify-between">
        <h3 className="font-semibold">Recommandations</h3>

        {/* Permet de relancer l'appel API à la demande */}
        <button 
          onClick={load} 
          className="text-sm text-gray-600 hover:underline"
        >
          Rafraîchir
        </button>
      </div>

      {/* Résumé généré par l'API (ex : analyse globale du produit) */}
      <p className="mt-2 text-sm text-gray-700">
        {data.summary}
      </p>

      {/* Affichage conditionnel des points faibles si existants */}
      {data.weak_points?.length > 0 && (
        <div className="mt-3">
          <div className="text-sm font-medium">
            Points faibles récurrents
          </div>

          {/* Affichage sous forme de tags */}
          <div className="mt-2 flex flex-wrap gap-2">
            {data.weak_points.map((w) => (
              <span 
                key={w} 
                className="rounded-full bg-gray-100 px-2 py-1 text-xs"
              >
                {w}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Liste d'actions recommandées par l'algorithme */}
      <div className="mt-3">
        <div className="text-sm font-medium">
          Actions (3–5)
        </div>

        <ul className="mt-2 list-disc pl-5 text-sm text-gray-700 space-y-1">
          {data.actions.map((a, idx) => (
            <li key={idx}>{a}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}