"use client";

import { useCallback, useMemo } from "react";
import { usePolling } from "@/hooks/usePolling";
import { api } from "@/lib/api";
import type { NewsItemWithAnalysis } from "@/lib/types";

function getColor(count: number, max: number): string {
  if (max === 0) return "bg-gray-100 text-gray-600 dark:bg-zinc-800 dark:text-zinc-400";
  const ratio = count / max;
  if (ratio > 0.7) return "bg-red-100 text-red-800 dark:bg-red-500/20 dark:text-red-400";
  if (ratio > 0.4) return "bg-yellow-100 text-yellow-800 dark:bg-yellow-500/20 dark:text-yellow-400";
  if (ratio > 0.15) return "bg-blue-100 text-blue-800 dark:bg-blue-500/20 dark:text-blue-400";
  return "bg-gray-100 text-gray-600 dark:bg-zinc-800 dark:text-zinc-400";
}

export function AssetHeatmap() {
  const fetcher = useCallback(() => api.getNews(100), []);
  const { data: news } = usePolling(fetcher, 15000);

  const assetCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    if (!news) return counts;
    for (const item of news) {
      if (item.analysis?.affected_assets) {
        for (const asset of item.analysis.affected_assets) {
          counts[asset] = (counts[asset] || 0) + 1;
        }
      }
    }
    return counts;
  }, [news]);

  const sorted = Object.entries(assetCounts).sort((a, b) => b[1] - a[1]);
  const max = sorted.length > 0 ? sorted[0][1] : 0;

  if (sorted.length === 0) {
    return (
      <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
        <h3 className="mb-3 text-sm font-medium text-gray-700 dark:text-zinc-300">
          Asset Mentions
        </h3>
        <p className="text-xs text-gray-400 dark:text-zinc-500">
          No asset data yet.
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
      <h3 className="mb-3 text-sm font-medium text-gray-700 dark:text-zinc-300">
        Asset Mentions
      </h3>
      <div className="flex flex-wrap gap-2">
        {sorted.map(([asset, count]) => (
          <span
            key={asset}
            className={`inline-flex items-center gap-1 rounded-lg px-2.5 py-1.5 text-xs font-medium ${getColor(count, max)}`}
          >
            {asset}
            <span className="opacity-70">{count}</span>
          </span>
        ))}
      </div>
    </div>
  );
}
