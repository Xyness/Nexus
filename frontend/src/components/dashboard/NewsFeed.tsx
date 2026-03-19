"use client";

import { useCallback } from "react";
import { usePolling } from "@/hooks/usePolling";
import { useSSE } from "@/hooks/useSSE";
import { api } from "@/lib/api";
import { Badge } from "@/components/ui/Badge";
import { Spinner } from "@/components/ui/Spinner";
import type { NewsItemWithAnalysis } from "@/lib/types";

function timeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const minutes = Math.floor(diff / 60000);
  if (minutes < 1) return "just now";
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}

export function NewsFeed() {
  const fetcher = useCallback(() => api.getNews(50), []);
  const { data: news, loading, error } = usePolling(fetcher, 10000);
  const { connected } = useSSE();

  if (loading && !news) {
    return (
      <div className="flex justify-center p-8">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-400">
        {error}
      </div>
    );
  }

  return (
    <div>
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-sm font-medium text-gray-700 dark:text-zinc-300">
          Live News Feed
        </h2>
        <div className="flex items-center gap-1.5">
          <span
            className={`h-2 w-2 rounded-full ${
              connected ? "bg-green-500" : "bg-red-500"
            }`}
          />
          <span className="text-xs text-gray-500 dark:text-zinc-500">
            {connected ? "Connected" : "Reconnecting..."}
          </span>
        </div>
      </div>

      <div className="max-h-[600px] space-y-2 overflow-y-auto rounded-xl border border-gray-200 bg-white p-3 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
        {news && news.length > 0 ? (
          news.map((item: NewsItemWithAnalysis) => (
            <NewsRow key={item.id} item={item} />
          ))
        ) : (
          <div className="p-6 text-center text-sm text-gray-400 dark:text-zinc-500">
            No news items yet. Waiting for first poll...
          </div>
        )}
      </div>
    </div>
  );
}

function NewsRow({ item }: { item: NewsItemWithAnalysis }) {
  const analysis = item.analysis;

  return (
    <a
      href={item.url}
      target="_blank"
      rel="noopener noreferrer"
      className="block rounded-lg border border-transparent p-3 transition-all hover:border-gray-200 hover:bg-gray-50 dark:hover:border-zinc-700 dark:hover:bg-zinc-800/50"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <p className="text-sm font-medium text-gray-900 dark:text-white line-clamp-2">
            {item.title}
          </p>
          <div className="mt-1.5 flex flex-wrap items-center gap-2">
            <span className="text-xs text-gray-500 dark:text-zinc-500">
              {item.source}
            </span>
            <span className="text-xs text-gray-400 dark:text-zinc-600">
              {timeAgo(item.fetched_at)}
            </span>
            {analysis && (
              <>
                <Badge label={analysis.urgency || "normal"} />
                <Badge label={analysis.sentiment || "neutral"} />
                {analysis.affected_assets?.map((asset) => (
                  <span
                    key={asset}
                    className="inline-flex items-center rounded-md bg-blue-50 px-1.5 py-0.5 text-xs font-medium text-blue-700 dark:bg-blue-500/10 dark:text-blue-400"
                  >
                    {asset}
                  </span>
                ))}
              </>
            )}
          </div>
          {analysis?.summary && (
            <p className="mt-1.5 text-xs text-gray-500 dark:text-zinc-400 line-clamp-1">
              {analysis.summary}
            </p>
          )}
        </div>
        {analysis && (
          <div className="flex flex-shrink-0 flex-col items-end">
            <span
              className={`text-lg font-bold ${
                analysis.relevance_score >= 7
                  ? "text-red-600 dark:text-red-400"
                  : analysis.relevance_score >= 4
                  ? "text-yellow-600 dark:text-yellow-400"
                  : "text-gray-400 dark:text-zinc-500"
              }`}
            >
              {analysis.relevance_score.toFixed(1)}
            </span>
            <span className="text-[10px] text-gray-400 dark:text-zinc-500">
              /10
            </span>
          </div>
        )}
      </div>
    </a>
  );
}
