"use client";

export function ThresholdConfig() {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
      <h2 className="mb-3 text-sm font-medium text-gray-700 dark:text-zinc-300">
        Alert Thresholds
      </h2>
      <div className="space-y-4">
        <div>
          <label className="block text-xs font-medium text-gray-600 dark:text-zinc-400">
            Default Relevance Threshold
          </label>
          <p className="mt-0.5 text-xs text-gray-400 dark:text-zinc-500">
            News scoring above this threshold will trigger alerts (set via ALERT_RELEVANCE_THRESHOLD env var)
          </p>
          <div className="mt-2 flex items-center gap-2">
            <div className="flex h-10 items-center rounded-lg border border-gray-300 bg-gray-50 px-4 text-sm text-gray-600 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-300">
              7.0 / 10
            </div>
            <span className="text-xs text-gray-400 dark:text-zinc-500">
              (configured server-side)
            </span>
          </div>
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-600 dark:text-zinc-400">
            Alert Cooldown
          </label>
          <p className="mt-0.5 text-xs text-gray-400 dark:text-zinc-500">
            Anti-spam: minimum time between alerts for the same asset
          </p>
          <div className="mt-2 flex h-10 items-center rounded-lg border border-gray-300 bg-gray-50 px-4 text-sm text-gray-600 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-300">
            30 minutes
          </div>
        </div>
      </div>
    </div>
  );
}
