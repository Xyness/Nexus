"use client";

import { useRouter } from "next/navigation";
import { Badge } from "@/components/ui/Badge";
import { MarkdownRenderer } from "./MarkdownRenderer";
import { Spinner } from "@/components/ui/Spinner";
import { api } from "@/lib/api";
import type { ReportDetail as ReportDetailType } from "@/lib/types";

function SentimentGauge({ score }: { score: number }) {
  const pct = Math.round(score * 100);
  const hue = score * 120; // 0=red, 60=yellow, 120=green
  return (
    <div className="flex flex-col items-center gap-1">
      <div className="relative h-28 w-28">
        <svg viewBox="0 0 100 100" className="h-full w-full -rotate-90">
          <circle
            cx="50" cy="50" r="42"
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-gray-200 dark:text-zinc-700"
          />
          <circle
            cx="50" cy="50" r="42"
            fill="none"
            stroke={`hsl(${hue}, 70%, 50%)`}
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={`${score * 264} 264`}
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-2xl font-bold text-gray-900 dark:text-white">{pct}</span>
        </div>
      </div>
      <span className="text-xs font-medium text-gray-500 dark:text-zinc-400">Sentiment Score</span>
    </div>
  );
}

export function ReportDetail({ report }: { report: ReportDetailType }) {
  const router = useRouter();

  const handleDelete = async () => {
    try {
      await api.deleteReport(report.id);
      router.push("/reports");
    } catch {
      // Ignore
    }
  };

  const isReady = report.status === "completed";

  return (
    <div className="space-y-8">
      {/* ── Header ── */}
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-3">
            <h1 className="truncate text-3xl font-bold tracking-tight text-gray-900 dark:text-white">
              {report.topic}
            </h1>
            {report.sentiment && <Badge label={report.sentiment} />}
          </div>
          <p className="mt-2 text-sm text-gray-500 dark:text-zinc-400">
            {new Date(report.created_at).toLocaleDateString("en-US", {
              weekday: "long",
              year: "numeric",
              month: "long",
              day: "numeric",
              hour: "2-digit",
              minute: "2-digit",
            })}
            {report.completed_at && (
              <>
                {" "}· Completed in{" "}
                {Math.round(
                  (new Date(report.completed_at).getTime() -
                    new Date(report.created_at).getTime()) /
                    1000
                )}
                s
              </>
            )}
          </p>
        </div>
        <button
          onClick={handleDelete}
          className="shrink-0 rounded-lg border border-red-200 px-3 py-2 text-sm font-medium text-red-600 transition-all hover:bg-red-50 hover:border-red-300 dark:border-red-500/20 dark:text-red-400 dark:hover:bg-red-500/10"
        >
          Delete Report
        </button>
      </div>

      {/* ── Metrics Bar ── */}
      {isReady && (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
          {report.sentiment_score !== null && (
            <div className="flex items-center justify-center rounded-2xl border border-gray-200 bg-white p-5 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
              <SentimentGauge score={report.sentiment_score} />
            </div>
          )}
          <div className="flex flex-col items-center justify-center rounded-2xl border border-gray-200 bg-white p-5 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
            <span className="text-3xl font-bold text-gray-900 dark:text-white">
              {report.sources_count}
            </span>
            <span className="mt-1 text-xs font-medium text-gray-500 dark:text-zinc-400">Sources Analyzed</span>
          </div>
          <div className="flex flex-col items-center justify-center rounded-2xl border border-gray-200 bg-white p-5 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
            <span className="text-3xl font-bold text-gray-900 dark:text-white">
              {report.sub_questions?.length ?? 0}
            </span>
            <span className="mt-1 text-xs font-medium text-gray-500 dark:text-zinc-400">Research Questions</span>
          </div>
          {report.sentiment && (
            <div className="flex flex-col items-center justify-center rounded-2xl border border-gray-200 bg-white p-5 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
              <span className={`text-3xl font-bold ${
                report.sentiment === "bullish"
                  ? "text-green-600 dark:text-green-400"
                  : report.sentiment === "bearish"
                  ? "text-red-600 dark:text-red-400"
                  : "text-yellow-600 dark:text-yellow-400"
              }`}>
                {report.sentiment === "bullish" ? "↑" : report.sentiment === "bearish" ? "↓" : "→"}
              </span>
              <span className="mt-1 text-xs font-medium text-gray-500 dark:text-zinc-400 capitalize">
                {report.sentiment}
              </span>
            </div>
          )}
        </div>
      )}

      {/* ── Research Questions ── */}
      {isReady && report.sub_questions && report.sub_questions.length > 0 && (
        <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
          <h2 className="mb-4 text-sm font-semibold uppercase tracking-wider text-gray-500 dark:text-zinc-400">
            Research Questions
          </h2>
          <div className="grid gap-3 sm:grid-cols-2">
            {report.sub_questions.map((q, i) => (
              <div
                key={i}
                className="flex items-start gap-3 rounded-xl bg-gray-50 p-3 dark:bg-zinc-800/50"
              >
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-brand-100 text-xs font-bold text-brand-700 dark:bg-brand-500/10 dark:text-brand-500">
                  {i + 1}
                </span>
                <span className="text-sm text-gray-700 dark:text-zinc-300">{q}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Report Content ── */}
      {report.content_md && (
        <div className="rounded-2xl border border-gray-200 bg-white p-8 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
          <h2 className="mb-6 text-sm font-semibold uppercase tracking-wider text-gray-500 dark:text-zinc-400">
            Full Analysis
          </h2>
          <MarkdownRenderer content={report.content_md} />
        </div>
      )}

      {/* ── Sources ── */}
      {isReady && report.sources && report.sources.length > 0 && (
        <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
          <h2 className="mb-4 text-sm font-semibold uppercase tracking-wider text-gray-500 dark:text-zinc-400">
            Sources
          </h2>
          <div className="grid gap-2 sm:grid-cols-2">
            {report.sources.map((source, i) => (
              <a
                key={i}
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex items-center gap-3 rounded-xl bg-gray-50 p-3 transition-all hover:bg-gray-100 dark:bg-zinc-800/50 dark:hover:bg-zinc-800"
              >
                <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-brand-100 text-xs font-bold text-brand-700 dark:bg-brand-500/10 dark:text-brand-500">
                  {i + 1}
                </span>
                <span className="min-w-0 flex-1">
                  <span className="block truncate text-sm font-medium text-gray-900 group-hover:text-brand-600 dark:text-white dark:group-hover:text-brand-500">
                    {source.title}
                  </span>
                  <span className="block truncate text-xs text-gray-400 dark:text-zinc-500">
                    {source.url}
                  </span>
                </span>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-4 w-4 shrink-0 text-gray-400 dark:text-zinc-500">
                  <path fillRule="evenodd" d="M4.25 5.5a.75.75 0 00-.75.75v8.5c0 .414.336.75.75.75h8.5a.75.75 0 00.75-.75v-4a.75.75 0 011.5 0v4A2.25 2.25 0 0112.75 17h-8.5A2.25 2.25 0 012 14.75v-8.5A2.25 2.25 0 014.25 4h5a.75.75 0 010 1.5h-5zm7.25-.75a.75.75 0 01.75-.75h3.5a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0V6.31l-5.47 5.47a.75.75 0 01-1.06-1.06l5.47-5.47H12.25a.75.75 0 01-.75-.75z" clipRule="evenodd" />
                </svg>
              </a>
            ))}
          </div>
        </div>
      )}

      {/* ── Error ── */}
      {report.error_message && (
        <div className="rounded-2xl border border-red-200 bg-red-50 p-5 dark:border-red-500/20 dark:bg-red-500/10">
          <h2 className="mb-2 text-sm font-semibold text-red-800 dark:text-red-400">Error</h2>
          <p className="text-sm text-red-700 dark:text-red-300">{report.error_message}</p>
        </div>
      )}

      {/* ── Loading state ── */}
      {(report.status === "pending" || report.status === "running") && (
        <div className="flex flex-col items-center justify-center gap-4 rounded-2xl border border-dashed border-gray-300 p-16 dark:border-zinc-700">
          <Spinner size="lg" />
          <p className="text-sm text-gray-500 dark:text-zinc-400">
            {report.status === "pending"
              ? "Queued — waiting to start analysis..."
              : "Researching and analyzing — this page updates automatically."}
          </p>
        </div>
      )}
    </div>
  );
}
