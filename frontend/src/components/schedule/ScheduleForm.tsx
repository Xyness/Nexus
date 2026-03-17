"use client";

import { useState } from "react";
import { api } from "@/lib/api";

export function ScheduleForm({ onCreated }: { onCreated?: () => void }) {
  const [topic, setTopic] = useState("");
  const [cron, setCron] = useState("0 9 * * *");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;
    setLoading(true);
    setError(null);
    try {
      await api.createSchedule(topic.trim(), cron.trim());
      setTopic("");
      onCreated?.();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to create schedule");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-zinc-300">Topic</label>
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="e.g. Bitcoin, Ethereum"
          className="mt-1 w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm shadow-sm transition-all duration-200 placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:border-zinc-700 dark:bg-zinc-800 dark:text-white dark:placeholder:text-zinc-500"
          disabled={loading}
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-zinc-300">
          Cron Expression
        </label>
        <input
          type="text"
          value={cron}
          onChange={(e) => setCron(e.target.value)}
          placeholder="0 9 * * *"
          className="mt-1 w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-mono shadow-sm transition-all duration-200 placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:border-zinc-700 dark:bg-zinc-800 dark:text-white dark:placeholder:text-zinc-500"
          disabled={loading}
        />
        <p className="mt-1 text-xs text-gray-400 dark:text-zinc-500">
          Format: minute hour day month day_of_week (e.g. &quot;0 9 * * *&quot; = every day at 9:00 AM)
        </p>
      </div>
      <button
        type="submit"
        disabled={loading || !topic.trim()}
        className="rounded-lg bg-brand-600 px-5 py-2 text-sm font-medium text-white shadow-sm transition-all duration-200 hover:bg-brand-700 hover:shadow-md disabled:opacity-50"
      >
        {loading ? "Creating..." : "Create Schedule"}
      </button>
      {error && <p className="text-sm text-red-600 dark:text-red-400">{error}</p>}
    </form>
  );
}
