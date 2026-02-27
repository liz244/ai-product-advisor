   import ProductsPage from "./pages/ProductsPage";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <header className="border-b bg-white">
        <div className="mx-auto max-w-6xl px-4 py-4">
          <h1 className="text-xl font-semibold">AI Product Advisor</h1>
          <p className="text-sm text-gray-500">
            Avis → Sentiment → Stats → Recommandations
          </p>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-6">
        <ProductsPage />
      </main>
    </div>
  );
}