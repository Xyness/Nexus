"use client";

import { useCallback } from "react";
import { usePolling } from "@/hooks/usePolling";
import { api } from "@/lib/api";
import type { SourceConfig } from "@/lib/types";

const TYPE_LABELS: Record<string, string> = {
  rss: "RSS",
  reddit: "Reddit",
  twitter: "Twitter/X",
};

export function SourcesManager() {
  const fetcher = useCallback(() => api.getSources(), []);
  const { data: sources, refresh } = usePolling(fetcher, 30000);

  const handleToggle = async (source: SourceConfig) => {
    try {
      await api.toggleSource(source.id, !source.enabled);
      refresh();
    } catch {
      // ignore
    }
  };

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
      <h2 className="mb-4 text-sm font-medium text-gray-700 dark:text-zinc-300">
        News Sources
      </h2>
      <div className="space-y-2">
        {sources?.map((source: SourceConfig) => (
          <div
            key={source.id}
            className="flex items-center justify-between rounded-lg border border-gray-100 p-3 dark:border-zinc-800"
          >
            <div className="flex items-center gap-3">
              <span className="inline-flex items-center rounded-md bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-600 dark:bg-zinc-800 dark:text-zinc-400">
                {TYPE_LABELS[source.type] || source.type}
              </span>
              <div>
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  {source.name}
                </p>
                {source.last_fetched && (
                  <p className="text-xs text-gray-400 dark:text-zinc-500">
                    Last fetched: {new Date(source.last_fetched).toLocaleString()}
                  </p>
                )}
              </div>
            </div>
            <button
              onClick={() => handleToggle(source)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                source.enabled
                  ? "bg-brand-600"
                  : "bg-gray-300 dark:bg-zinc-700"
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  source.enabled ? "translate-x-6" : "translate-x-1"
                }`}
              />
            </button>
          </div>
        ))}
        {(!sources || sources.length === 0) && (
          <p className="text-sm text-gray-400 dark:text-zinc-500">
            No sources configured.
          </p>
        )}
      </div>
    </div>
  );
}
