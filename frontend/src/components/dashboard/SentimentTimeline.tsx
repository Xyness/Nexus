"use client";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import { useTheme } from "@/hooks/useTheme";
import type { ReportSummary } from "@/lib/types";

export function SentimentTimeline({ reports }: { reports: ReportSummary[] }) {
  const { theme } = useTheme();
  const isDark = theme === "dark";

  const completed = reports
    .filter((r) => r.status === "completed" && r.sentiment_score !== null)
    .reverse()
    .map((r) => ({
      date: new Date(r.created_at).toLocaleDateString(),
      topic: r.topic,
      score: Math.round((r.sentiment_score ?? 0.5) * 100),
    }));

  if (completed.length < 2) {
    return (
      <div className="flex h-48 items-center justify-center rounded-lg border border-dashed border-gray-300 text-sm text-gray-400 dark:border-zinc-700 dark:text-zinc-500">
        Complete at least 2 watches to see the sentiment timeline
      </div>
    );
  }

  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={completed}>
          <CartesianGrid strokeDasharray="3 3" stroke={isDark ? "#3f3f46" : "#e5e7eb"} />
          <XAxis dataKey="date" tick={{ fontSize: 12, fill: isDark ? "#a1a1aa" : "#6b7280" }} />
          <YAxis domain={[0, 100]} tick={{ fontSize: 12, fill: isDark ? "#a1a1aa" : "#6b7280" }} />
          <Tooltip
            contentStyle={{
              backgroundColor: isDark ? "#18181b" : "#ffffff",
              borderColor: isDark ? "#3f3f46" : "#e5e7eb",
              borderRadius: "0.5rem",
              color: isDark ? "#f4f4f5" : "#111827",
            }}
            formatter={(value: number) => [`${value}%`, "Sentiment"]}
            labelFormatter={(label) => {
              const point = completed.find((c) => c.date === label);
              return point ? `${point.topic} — ${label}` : label;
            }}
          />
          <Line
            type="monotone"
            dataKey="score"
            stroke={isDark ? "#60a5fa" : "#2563eb"}
            strokeWidth={2}
            dot={{ r: 4, fill: isDark ? "#60a5fa" : "#2563eb" }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
