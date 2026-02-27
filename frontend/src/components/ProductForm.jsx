import { useState } from "react";
import { api } from "../api";

export default function ProductForm({ onCreated }) {
  const [name, setName] = useState("");
  const [category, setCategory] = useState("");
  const [error, setError] = useState("");

  async function submit(e) {
    e.preventDefault();
    setError("");
    try {
      await api.post("/products", { name, category });
      setName("");
      setCategory("");
      onCreated?.();
    } catch (err) {
      setError(err?.response?.data?.error || "Erreur");
    }
  }

  return (
    <form onSubmit={submit} className="rounded-2xl bg-white p-4 shadow-sm border space-y-3">
      <h3 className="font-semibold">Ajouter un produit</h3>
      <input
        className="w-full rounded-xl border px-3 py-2"
        placeholder="Nom"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        className="w-full rounded-xl border px-3 py-2"
        placeholder="Catégorie (audio, sport, maison...)"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
      />
      {error && <p className="text-sm text-red-600">{error}</p>}
      <button className="w-full rounded-xl bg-gray-900 px-3 py-2 text-white hover:bg-black">
        Ajouter
      </button>
    </form>
  );
}