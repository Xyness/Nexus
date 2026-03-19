"use client";

import { useState } from "react";
import { api } from "@/lib/api";

export function WatchlistForm({ onAdded }: { onAdded?: () => void }) {
  const [symbol, setSymbol] = useState("");
  const [threshold, setThreshold] = useState("5.0");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!symbol.trim()) return;

    setLoading(true);
    setError(null);
    try {
      await api.addToWatchlist(symbol.trim().toUpperCase(), parseFloat(threshold));
      setSymbol("");
      setThreshold("5.0");
      onAdded?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-wrap gap-3">
      <input
        type="text"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        placeholder="e.g. BTC, ETH, SOL..."
        className="flex-1 min-w-[120px] rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm shadow-sm placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:border-zinc-700 dark:bg-zinc-800 dark:text-white dark:placeholder:text-zinc-500"
        disabled={loading}
      />
      <input
        type="number"
        value={threshold}
        onChange={(e) => setThreshold(e.target.value)}
        min="0"
        max="10"
        step="0.5"
        className="w-24 rounded-lg border border-gray-300 bg-white px-3 py-2.5 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:border-zinc-700 dark:bg-zinc-800 dark:text-white"
        disabled={loading}
      />
      <button
        type="submit"
        disabled={loading || !symbol.trim()}
        className="rounded-lg bg-brand-600 px-5 py-2.5 text-sm font-medium text-white shadow-sm hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading ? "Adding..." : "Add"}
      </button>
      {error && (
        <p className="w-full text-sm text-red-600 dark:text-red-400">{error}</p>
      )}
    </form>
  );
}
