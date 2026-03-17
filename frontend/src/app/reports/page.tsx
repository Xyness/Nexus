"use client";

import { ReportList } from "@/components/reports/ReportList";
import { Spinner } from "@/components/ui/Spinner";
import { useReports } from "@/hooks/useReports";

export default function ReportsPage() {
  const { data: reports, loading, error, refresh } = useReports();

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Reports</h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-zinc-400">
          All generated market intelligence reports.
        </p>
      </div>

      {loading && !reports ? (
        <div className="flex justify-center p-8">
          <Spinner size="lg" />
        </div>
      ) : error ? (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-400">
          {error}
        </div>
      ) : (
        <ReportList reports={reports || []} onDeleted={refresh} />
      )}
    </div>
  );
}
