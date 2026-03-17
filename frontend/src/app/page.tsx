"use client";

import { WatchTrigger } from "@/components/dashboard/WatchTrigger";
import { ReportCard } from "@/components/dashboard/ReportCard";
import { SentimentTimeline } from "@/components/dashboard/SentimentTimeline";
import { Spinner } from "@/components/ui/Spinner";
import { useReports } from "@/hooks/useReports";

export default function DashboardPage() {
  const { data: reports, loading, error, refresh } = useReports();

  return (
    <div className="mx-auto max-w-5xl space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-zinc-400">
          Trigger a market watch to get an AI-powered analysis report.
        </p>
      </div>

      {/* Watch trigger */}
      <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
        <h2 className="mb-3 text-sm font-medium text-gray-700 dark:text-zinc-300">New Watch</h2>
        <WatchTrigger onTriggered={refresh} />
      </div>

      {/* Sentiment Timeline */}
      {reports && reports.length > 0 && (
        <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
          <h2 className="mb-3 text-sm font-medium text-gray-700 dark:text-zinc-300">
            Sentiment Timeline
          </h2>
          <SentimentTimeline reports={reports} />
        </div>
      )}

      {/* Recent reports */}
      <div>
        <h2 className="mb-3 text-sm font-medium text-gray-700 dark:text-zinc-300">
          Recent Reports
        </h2>
        {loading && !reports ? (
          <div className="flex justify-center p-8">
            <Spinner size="lg" />
          </div>
        ) : error ? (
          <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-400">
            {error}
          </div>
        ) : reports && reports.length > 0 ? (
          <div className="grid gap-4 sm:grid-cols-2">
            {reports.slice(0, 6).map((report) => (
              <ReportCard key={report.id} report={report} onDeleted={refresh} />
            ))}
          </div>
        ) : (
          <div className="rounded-lg border border-dashed border-gray-300 p-8 text-center text-sm text-gray-400 dark:border-zinc-700 dark:text-zinc-500">
            No reports yet. Start your first watch above!
          </div>
        )}
      </div>
    </div>
  );
}
