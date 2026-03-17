"use client";

import { useRouter } from "next/navigation";
import { Badge } from "@/components/ui/Badge";
import { StatusIndicator } from "@/components/ui/StatusIndicator";
import { api } from "@/lib/api";
import type { ReportSummary } from "@/lib/types";

export function ReportCard({
  report,
  onDeleted,
}: {
  report: ReportSummary;
  onDeleted?: () => void;
}) {
  const router = useRouter();

  const handleClick = () => {
    router.push(`/reports/${report.id}`);
  };

  const handleDelete = async (e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await api.deleteReport(report.id);
      onDeleted?.();
    } catch {
      // Ignore
    }
  };

  return (
    <div
      onClick={handleClick}
      className="relative cursor-pointer rounded-xl border border-gray-200 bg-white p-4 shadow-sm transition-all duration-200 hover:shadow-md dark:border-zinc-800 dark:bg-zinc-900"
    >
      <button
        onClick={handleDelete}
        className="absolute right-2 top-2 z-10 rounded-md p-1.5 text-gray-400 transition-all hover:bg-red-50 hover:text-red-600 dark:text-zinc-500 dark:hover:bg-red-500/10 dark:hover:text-red-400"
        aria-label="Delete report"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-4 w-4">
          <path fillRule="evenodd" d="M8.75 1A2.75 2.75 0 006 3.75v.443c-.795.077-1.584.176-2.365.298a.75.75 0 10.23 1.482l.149-.022.841 10.518A2.75 2.75 0 007.596 19h4.807a2.75 2.75 0 002.742-2.53l.841-10.519.149.023a.75.75 0 00.23-1.482A41.03 41.03 0 0014 4.193V3.75A2.75 2.75 0 0011.25 1h-2.5zM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4zM8.58 7.72a.75.75 0 00-1.5.06l.3 7.5a.75.75 0 101.5-.06l-.3-7.5zm4.34.06a.75.75 0 10-1.5-.06l-.3 7.5a.75.75 0 101.5.06l.3-7.5z" clipRule="evenodd" />
        </svg>
      </button>
      <div className="flex items-start justify-between pr-6">
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-gray-900 truncate dark:text-white">{report.topic}</h3>
          <p className="mt-1 text-xs text-gray-500 dark:text-zinc-500">
            {new Date(report.created_at).toLocaleString()}
          </p>
        </div>
        <StatusIndicator status={report.status} />
      </div>
      {report.status === "completed" && (
        <div className="mt-3 flex items-center gap-3">
          {report.sentiment && <Badge label={report.sentiment} />}
          {report.sentiment_score !== null && (
            <span className="text-xs text-gray-500 dark:text-zinc-500">
              Score: {(report.sentiment_score * 100).toFixed(0)}%
            </span>
          )}
          <span className="text-xs text-gray-500 dark:text-zinc-500">
            {report.sources_count} sources
          </span>
        </div>
      )}
    </div>
  );
}
