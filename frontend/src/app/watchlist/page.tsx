"use client";

import { WatchlistForm } from "@/components/watchlist/WatchlistForm";
import { WatchlistTable } from "@/components/watchlist/WatchlistTable";
import { useWatchlist } from "@/hooks/useWatchlist";

export default function WatchlistPage() {
  const { data: items, refresh } = useWatchlist();

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Watchlist
        </h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-zinc-400">
          Assets you&apos;re tracking. Lower thresholds mean more alerts for that asset.
        </p>
      </div>

      <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
        <h2 className="mb-3 text-sm font-medium text-gray-700 dark:text-zinc-300">
          Add Asset
        </h2>
        <WatchlistForm onAdded={refresh} />
      </div>

      <WatchlistTable items={items || []} onRemoved={refresh} />
    </div>
  );
}
