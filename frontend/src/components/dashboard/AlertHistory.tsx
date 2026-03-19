"use client";

import { useAlerts } from "@/hooks/useAlerts";
import { Badge } from "@/components/ui/Badge";
import { Spinner } from "@/components/ui/Spinner";
import type { AlertResponse } from "@/lib/types";

function timeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const minutes = Math.floor(diff / 60000);
  if (minutes < 1) return "just now";
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}

export function AlertHistory({ limit = 20 }: { limit?: number }) {
  const { data: alerts, loading, error } = useAlerts(limit);

  if (loading && !alerts) {
    return (
      <div className="flex justify-center p-8">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-400">
        {error}
      </div>
    );
  }

  if (!alerts || alerts.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-gray-300 p-6 text-center text-sm text-gray-400 dark:border-zinc-700 dark:text-zinc-500">
        No alerts yet.
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {alerts.map((alert: AlertResponse) => (
        <div
          key={alert.id}
          className="rounded-lg border border-gray-200 bg-white p-3 shadow-sm dark:border-zinc-800 dark:bg-zinc-900"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              {alert.analysis && (
                <>
                  <Badge label={alert.analysis.urgency || "normal"} />
                  <Badge label={alert.analysis.sentiment || "neutral"} />
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    {alert.analysis.relevance_score.toFixed(1)}/10
                  </span>
                </>
              )}
            </div>
            <span className="text-xs text-gray-500 dark:text-zinc-500">
              {timeAgo(alert.sent_at)} via {alert.channel}
            </span>
          </div>
          {alert.analysis?.summary && (
            <p className="mt-2 text-sm text-gray-600 dark:text-zinc-400">
              {alert.analysis.summary}
            </p>
          )}
          {alert.analysis?.affected_assets && (
            <div className="mt-2 flex flex-wrap gap-1">
              {alert.analysis.affected_assets.map((asset) => (
                <span
                  key={asset}
                  className="inline-flex items-center rounded-md bg-blue-50 px-1.5 py-0.5 text-xs font-medium text-blue-700 dark:bg-blue-500/10 dark:text-blue-400"
                >
                  {asset}
                </span>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
