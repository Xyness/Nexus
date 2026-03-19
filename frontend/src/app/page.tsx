"use client";

import { DailyStats } from "@/components/dashboard/DailyStats";
import { NewsFeed } from "@/components/dashboard/NewsFeed";
import { AssetHeatmap } from "@/components/dashboard/AssetHeatmap";
import { WatchTrigger } from "@/components/dashboard/WatchTrigger";
import { useReports } from "@/hooks/useReports";

export default function DashboardPage() {
  const { refresh } = useReports();

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Dashboard
        </h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-zinc-400">
          Real-time crypto & finance surveillance powered by AI.
        </p>
      </div>

      {/* Daily Stats */}
      <DailyStats />

      {/* Main content: News Feed + Sidebar */}
      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <NewsFeed />
        </div>
        <div className="space-y-6">
          <AssetHeatmap />

          {/* Quick Watch */}
          <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
            <h3 className="mb-3 text-sm font-medium text-gray-700 dark:text-zinc-300">
              Quick Report
            </h3>
            <WatchTrigger onTriggered={refresh} />
          </div>
        </div>
      </div>
    </div>
  );
}
