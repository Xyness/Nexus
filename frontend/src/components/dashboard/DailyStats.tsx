"use client";

import { useCallback } from "react";
import { usePolling } from "@/hooks/usePolling";
import { api } from "@/lib/api";
import type { DailyStatsResponse } from "@/lib/types";

function StatCard({
  label,
  value,
  color,
}: {
  label: string;
  value: number | string;
  color?: string;
}) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
      <p className="text-xs font-medium text-gray-500 dark:text-zinc-400">
        {label}
      </p>
      <p className={`mt-1 text-2xl font-bold ${color || "text-gray-900 dark:text-white"}`}>
        {value}
      </p>
    </div>
  );
}

export function DailyStats() {
  const fetcher = useCallback(() => api.getDailyStats(), []);
  const { data: stats } = usePolling(fetcher, 15000);

  const s: DailyStatsResponse = stats || {
    total_news: 0,
    analyzed_news: 0,
    alerts_sent: 0,
    bullish_count: 0,
    bearish_count: 0,
    neutral_count: 0,
    active_sources: 0,
  };

  const sentimentRatio =
    s.bullish_count + s.bearish_count > 0
      ? `${s.bullish_count}B / ${s.bearish_count}R`
      : "-";

  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
      <StatCard label="Alerts Today" value={s.alerts_sent} color="text-red-600 dark:text-red-400" />
      <StatCard label="News Analyzed" value={s.analyzed_news} />
      <StatCard label="Sentiment" value={sentimentRatio} />
      <StatCard label="Active Sources" value={s.active_sources} color="text-green-600 dark:text-green-400" />
    </div>
  );
}
