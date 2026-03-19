"use client";

import { api } from "@/lib/api";
import type { WatchlistItem } from "@/lib/types";

export function WatchlistTable({
  items,
  onRemoved,
}: {
  items: WatchlistItem[];
  onRemoved?: () => void;
}) {
  const handleRemove = async (id: string) => {
    try {
      await api.removeFromWatchlist(id);
      onRemoved?.();
    } catch {
      // ignore
    }
  };

  if (items.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-gray-300 p-8 text-center text-sm text-gray-400 dark:border-zinc-700 dark:text-zinc-500">
        No assets in your watchlist. Add one above!
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-200 bg-gray-50 dark:border-zinc-800 dark:bg-zinc-800/50">
            <th className="px-4 py-3 text-left font-medium text-gray-600 dark:text-zinc-400">
              Asset
            </th>
            <th className="px-4 py-3 text-left font-medium text-gray-600 dark:text-zinc-400">
              Threshold
            </th>
            <th className="px-4 py-3 text-left font-medium text-gray-600 dark:text-zinc-400">
              Added
            </th>
            <th className="px-4 py-3 text-right font-medium text-gray-600 dark:text-zinc-400">
              Action
            </th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr
              key={item.id}
              className="border-b border-gray-100 last:border-0 dark:border-zinc-800"
            >
              <td className="px-4 py-3 font-medium text-gray-900 dark:text-white">
                {item.asset_symbol}
              </td>
              <td className="px-4 py-3 text-gray-600 dark:text-zinc-400">
                {item.alert_threshold}/10
              </td>
              <td className="px-4 py-3 text-gray-500 dark:text-zinc-500">
                {new Date(item.created_at).toLocaleDateString()}
              </td>
              <td className="px-4 py-3 text-right">
                <button
                  onClick={() => handleRemove(item.id)}
                  className="text-xs text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
                >
                  Remove
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
