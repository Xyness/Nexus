"use client";

import { useCallback } from "react";
import { api } from "@/lib/api";
import { usePolling } from "@/hooks/usePolling";
import { ScheduleForm } from "@/components/schedule/ScheduleForm";
import { ScheduleList } from "@/components/schedule/ScheduleList";
import { Spinner } from "@/components/ui/Spinner";

export default function SchedulePage() {
  const fetcher = useCallback(() => api.getSchedules(), []);
  const { data: schedules, loading, error, refresh } = usePolling(fetcher, 10000);

  return (
    <div className="mx-auto max-w-4xl space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Scheduled Watches</h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-zinc-400">
          Set up recurring market watches with cron expressions.
        </p>
      </div>

      <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
        <h2 className="mb-4 text-sm font-medium text-gray-700 dark:text-zinc-300">
          New Schedule
        </h2>
        <ScheduleForm onCreated={refresh} />
      </div>

      <div>
        <h2 className="mb-3 text-sm font-medium text-gray-700 dark:text-zinc-300">
          Active Schedules
        </h2>
        {loading && !schedules ? (
          <div className="flex justify-center p-8">
            <Spinner size="lg" />
          </div>
        ) : error ? (
          <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-400">
            {error}
          </div>
        ) : (
          <ScheduleList schedules={schedules || []} onDeleted={refresh} />
        )}
      </div>
    </div>
  );
}
