"use client";

import { useState } from "react";
import { useWatch } from "@/hooks/useWatch";

export function WatchTrigger({ onTriggered }: { onTriggered?: () => void }) {
  const [topic, setTopic] = useState("");
  const { trigger, loading, error } = useWatch();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;
    const id = await trigger(topic.trim());
    if (id) {
      setTopic("");
      onTriggered?.();
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-3">
      <input
        type="text"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="e.g. Bitcoin, Ethereum ETF, S&P 500..."
        className="flex-1 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm shadow-sm transition-all duration-200 placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:border-zinc-700 dark:bg-zinc-800 dark:text-white dark:placeholder:text-zinc-500 dark:focus:border-brand-500"
        disabled={loading}
      />
      <button
        type="submit"
        disabled={loading || !topic.trim()}
        className="rounded-lg bg-brand-600 px-5 py-2.5 text-sm font-medium text-white shadow-sm transition-all duration-200 hover:bg-brand-700 hover:shadow-md disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading ? "Launching..." : "Start Watch"}
      </button>
      {error && <p className="text-sm text-red-600 dark:text-red-400">{error}</p>}
    </form>
  );
}
