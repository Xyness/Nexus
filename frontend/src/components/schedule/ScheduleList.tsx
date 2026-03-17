"use client";

import { api } from "@/lib/api";
import type { Schedule } from "@/lib/types";

export function ScheduleList({
  schedules,
  onDeleted,
}: {
  schedules: Schedule[];
  onDeleted?: () => void;
}) {
  const handleDelete = async (id: string) => {
    try {
      await api.deleteSchedule(id);
      onDeleted?.();
    } catch {
      // Ignore
    }
  };

  if (schedules.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-gray-300 p-8 text-center text-sm text-gray-400 dark:border-zinc-700 dark:text-zinc-500">
        No scheduled watches yet.
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-xl border border-gray-200 shadow-sm dark:border-zinc-800">
      <table className="min-w-full divide-y divide-gray-200 dark:divide-zinc-800">
        <thead className="bg-gray-50 dark:bg-zinc-800/50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500 dark:text-zinc-400">
              Topic
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500 dark:text-zinc-400">
              Cron
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500 dark:text-zinc-400">
              Last Run
            </th>
            <th className="px-4 py-3" />
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200 bg-white dark:divide-zinc-800 dark:bg-zinc-900">
          {schedules.map((s) => (
            <tr key={s.id} className="transition-colors hover:bg-gray-50 dark:hover:bg-zinc-800/50">
              <td className="px-4 py-3 text-sm font-medium text-gray-900 dark:text-white">
                {s.topic}
              </td>
              <td className="px-4 py-3 text-sm font-mono text-gray-600 dark:text-zinc-400">
                {s.cron_expression}
              </td>
              <td className="px-4 py-3 text-sm text-gray-500 dark:text-zinc-500">
                {s.last_run_at
                  ? new Date(s.last_run_at).toLocaleString()
                  : "Never"}
              </td>
              <td className="px-4 py-3 text-right">
                <button
                  onClick={() => handleDelete(s.id)}
                  className="text-sm text-red-600 transition-colors hover:text-red-800 dark:text-red-400 dark:hover:text-red-300"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
