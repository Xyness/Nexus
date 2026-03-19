"use client";

import { AlertHistory } from "@/components/dashboard/AlertHistory";

export default function AlertsPage() {
  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Alert History
        </h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-zinc-400">
          View all alerts sent by Nexus when relevant news is detected.
        </p>
      </div>
      <AlertHistory limit={100} />
    </div>
  );
}
