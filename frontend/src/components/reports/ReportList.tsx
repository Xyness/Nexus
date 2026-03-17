import { ReportCard } from "@/components/dashboard/ReportCard";
import type { ReportSummary } from "@/lib/types";

export function ReportList({
  reports,
  onDeleted,
}: {
  reports: ReportSummary[];
  onDeleted?: () => void;
}) {
  if (reports.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-gray-300 p-8 text-center text-sm text-gray-400 dark:border-zinc-700 dark:text-zinc-500">
        No reports yet. Start a watch from the dashboard.
      </div>
    );
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {reports.map((report) => (
        <ReportCard key={report.id} report={report} onDeleted={onDeleted} />
      ))}
    </div>
  );
}
