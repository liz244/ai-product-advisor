
import { useEffect, useState } from "react";
import { api } from "../api";

// Import des composants de la librairie Recharts pour la visualisation
import { PieChart, Pie, Tooltip, Legend, Cell } from "recharts";

/*
  Objet qui définit les couleurs associées à chaque type de sentiment.
  Cela permet de garder une cohérence visuelle dans le graphique.
*/
const COLORS = {
  positive: "#10873c", // vert
  neutral: "#7a7e84",  // gris
  negative: "#de0707", // rouge
};

export default function StatsCard({ productId }) {

  // State qui va contenir les statistiques retournées par l'API
  const [stats, setStats] = useState(null);

  /*
    Fonction qui récupère les statistiques du produit :
    - nombre total d’avis
    - moyenne des notes
    - répartition des sentiments (positive, neutral, negative)
  */
  async function load() {
    try {
      const { data } = await api.get(`/products/${productId}/stats`);
      setStats(data); // Mise à jour du state avec les données reçues
    } catch (error) {
      console.error("Erreur chargement stats:", error);
    }
  }

  /*
    useEffect permet de charger les statistiques
    à chaque fois que le produit sélectionné change.
  */
  useEffect(() => {
    if (productId) {
      load();
    }
  }, [productId]);

  // Affichage d’un état de chargement tant que les données ne sont pas disponibles
  if (!stats) {
    return (
      <div className="rounded-2xl bg-white p-5 shadow-md border border-gray-100 hover:shadow-lg transition">
        Chargement stats…
      </div>
    );
  }

  /*
    Préparation des données pour le graphique.
    Recharts attend un tableau d’objets avec :
    - name (label)
    - value (valeur numérique)
  */
  const chartData = [
    { name: "positive", value: stats.sentiments.positive },
    { name: "neutral", value: stats.sentiments.neutral },
    { name: "negative", value: stats.sentiments.negative },
  ];

  return (
    <div className="rounded-2xl bg-white p-4 shadow-sm border">
      <h3 className="font-semibold">Statistiques</h3>

      {/* Informations générales */}
      <div className="mt-2 text-sm text-gray-700 space-y-1">
        <div>
          Total avis: <b>{stats.total_reviews}</b>
        </div>
        <div>
          Moyenne notes: <b>{stats.avg_rating}</b>
        </div>
      </div>

      {/* Graphique circulaire représentant la répartition des sentiments */}
      <div className="mt-4 flex justify-center">
        <PieChart width={320} height={220}>
          <Pie
            data={chartData}
            dataKey="value"     // valeur numérique
            nameKey="name"      // label
            outerRadius={80}    // taille du cercle
          >
            {/* Attribution dynamique des couleurs */}
            {chartData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[entry.name]}
              />
            ))}
          </Pie>

          {/* Tooltip = info au survol */}
          <Tooltip />

          {/* Legend = affichage des labels sous le graphique */}
          <Legend />
        </PieChart>
      </div>
    </div>
  );
}