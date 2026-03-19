"use client";

import { useCallback } from "react";
import { usePolling } from "@/hooks/usePolling";
import { api } from "@/lib/api";
import { SourcesManager } from "@/components/settings/SourcesManager";
import { ThresholdConfig } from "@/components/settings/ThresholdConfig";

export default function SettingsPage() {
  const healthFetcher = useCallback(
    () => fetch((process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000") + "/health").then((r) => r.json()),
    []
  );
  const { data: health } = usePolling(healthFetcher, 30000);

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Settings
        </h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-zinc-400">
          Configure sources, thresholds, and system settings.
        </p>
      </div>

      {/* System Status */}
      <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
        <h2 className="mb-3 text-sm font-medium text-gray-700 dark:text-zinc-300">
          System Status
        </h2>
        {health ? (
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            <StatusItem label="Service" value={health.service || "nexus"} ok />
            <StatusItem label="Mode" value={health.mock_mode ? "Mock" : "Live"} ok={!health.mock_mode} />
            <StatusItem label="Telegram" value={health.telegram_enabled ? "On" : "Off"} ok={health.telegram_enabled} />
            <StatusItem label="Reddit" value={health.reddit_enabled ? "On" : "Off"} ok={health.reddit_enabled} />
          </div>
        ) : (
          <p className="text-sm text-gray-400">Loading...</p>
        )}
      </div>

      <ThresholdConfig />
      <SourcesManager />
    </div>
  );
}

function StatusItem({
  label,
  value,
  ok,
}: {
  label: string;
  value: string;
  ok: boolean;
}) {
  return (
    <div className="flex items-center gap-2">
      <span className={`h-2 w-2 rounded-full ${ok ? "bg-green-500" : "bg-yellow-500"}`} />
      <div>
        <p className="text-xs text-gray-500 dark:text-zinc-400">{label}</p>
        <p className="text-sm font-medium text-gray-900 dark:text-white">{value}</p>
      </div>
    </div>
  );
}
