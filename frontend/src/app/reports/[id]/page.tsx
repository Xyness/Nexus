"use client";

import { useCallback } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";
import { usePolling } from "@/hooks/usePolling";
import { ReportDetail } from "@/components/reports/ReportDetail";
import { Spinner } from "@/components/ui/Spinner";

export default function ReportDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const fetcher = useCallback(() => api.getReport(id), [id]);
  const { data: report, loading, error } = usePolling(fetcher, 3000);

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <Link
        href="/reports"
        className="inline-flex items-center text-sm text-gray-500 transition-colors hover:text-gray-700 dark:text-zinc-400 dark:hover:text-zinc-200"
      >
        &larr; Back to Reports
      </Link>

      {loading && !report ? (
        <div className="flex justify-center p-12">
          <Spinner size="lg" />
        </div>
      ) : error ? (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-400">
          {error}
        </div>
      ) : report ? (
        <ReportDetail report={report} />
      ) : null}
    </div>
  );
}
