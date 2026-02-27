import { useEffect, useMemo, useState } from "react";
import { api } from "../api";
import ProductForm from "../components/ProductForm";
import ReviewForm from "../components/ReviewForm";
import ReviewsList from "../components/ReviewsList";
import StatsCard from "../components/StatsCard";
import Recommendations from "../components/Recommendations";

export default function ProductsPage() {
  const [products, setProducts] = useState([]);
  const [selectedId, setSelectedId] = useState(null);

  const selected = useMemo(
    () => products.find((p) => p.id === selectedId) || null,
    [products, selectedId]
  );

  async function loadProducts() {
    try {
      const { data } = await api.get("/products");
      setProducts(data);
      if (data.length && !selectedId) setSelectedId(data[0].id);
    } catch (error) {
      console.error("Erreur chargement produits:", error);
    }
  }

  async function deleteProduct(id) {
    try {
      await api.delete(`/products/${id}`);
      await loadProducts();
      if (id === selectedId) setSelectedId(null);
    } catch (error) {
      console.error("Erreur suppression produit:", error);
    }
  }

  useEffect(() => {
    loadProducts();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="w-full">
      {/* Layout principal mobile-first */}
      <div className="grid gap-6 grid-cols-1 lg:grid-cols-3">

        {/* ================= LEFT COLUMN ================= */}
        <section className="space-y-4 lg:col-span-1">
          <div className="rounded-2xl bg-white p-4 shadow-sm border">
            <h2 className="font-semibold text-lg">Produits</h2>

            <div className="mt-3 space-y-2">
              {products.map((p) => (
                <button
                  key={p.id}
                  onClick={() => setSelectedId(p.id)}
                  className={`w-full rounded-xl border px-3 py-3 text-left transition hover:bg-gray-50 ${
                    selectedId === p.id
                      ? "border-gray-900 bg-gray-50"
                      : "border-gray-200"
                  }`}
                >
                  <div className="flex items-center justify-between gap-2">
                    <div>
                      <div className="font-medium">{p.name}</div>
                      <div className="text-xs text-gray-500">
                        {p.category}
                      </div>
                    </div>

                    <span
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteProduct(p.id);
                      }}
                      className="text-xs text-red-600 hover:underline"
                    >
                      Supprimer
                    </span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          <ProductForm onCreated={loadProducts} />
        </section>

        {/* ================= RIGHT COLUMN ================= */}
        <section className="space-y-6 lg:col-span-2">

          {!selected ? (
            <div className="rounded-2xl bg-white p-6 shadow-sm border text-center">
              Sélectionne un produit.
            </div>
          ) : (
            <>
              {/* Product Header */}
              <div className="rounded-2xl bg-white p-4 shadow-sm border">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                  <div>
                    <h2 className="text-lg font-semibold">
                      {selected.name}
                    </h2>
                    <p className="text-sm text-gray-500">
                      {selected.category}
                    </p>
                  </div>
                </div>
              </div>

              {/* Stats + Recommendations responsive */}
              <div className="grid gap-6 grid-cols-1 md:grid-cols-2">
                <StatsCard productId={selected.id} />
                <Recommendations productId={selected.id} />
              </div>

              {/* Review Form */}
              <ReviewForm productId={selected.id} onAdded={() => {}} />

              {/* Reviews List */}
              <ReviewsList productId={selected.id} />
            </>
          )}
        </section>
      </div>
    </div>
  );
}