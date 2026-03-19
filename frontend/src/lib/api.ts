const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchApi<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

export const api = {
  // --- Watch (legacy) ---
  triggerWatch: (topic: string) =>
    fetchApi<{ report_id: string; status: string }>("/watch", {
      method: "POST",
      body: JSON.stringify({ topic }),
    }),

  getReports: () => fetchApi<import("./types").ReportSummary[]>("/reports"),

  getReport: (id: string) =>
    fetchApi<import("./types").ReportDetail>(`/reports/${id}`),

  createSchedule: (topic: string, cron_expression: string) =>
    fetchApi<import("./types").Schedule>("/schedule", {
      method: "POST",
      body: JSON.stringify({ topic, cron_expression }),
    }),

  getSchedules: () => fetchApi<import("./types").Schedule[]>("/schedule"),

  deleteSchedule: (id: string) =>
    fetchApi<{ status: string }>(`/schedule/${id}`, { method: "DELETE" }),

  deleteReport: (id: string) =>
    fetchApi<{ status: string }>(`/reports/${id}`, { method: "DELETE" }),

  // --- Nexus endpoints ---
  getNews: (limit = 50, offset = 0) =>
    fetchApi<import("./types").NewsItemWithAnalysis[]>(
      `/news?limit=${limit}&offset=${offset}`
    ),

  getAlerts: (limit = 50, offset = 0) =>
    fetchApi<import("./types").AlertResponse[]>(
      `/alerts?limit=${limit}&offset=${offset}`
    ),

  getDailyStats: () =>
    fetchApi<import("./types").DailyStatsResponse>("/news/stats/daily"),

  getWatchlist: () =>
    fetchApi<import("./types").WatchlistItem[]>("/watchlist"),

  addToWatchlist: (asset_symbol: string, alert_threshold = 5.0) =>
    fetchApi<import("./types").WatchlistItem>("/watchlist", {
      method: "POST",
      body: JSON.stringify({ asset_symbol, alert_threshold }),
    }),

  removeFromWatchlist: (id: string) =>
    fetchApi<{ status: string }>(`/watchlist/${id}`, { method: "DELETE" }),

  getSources: () =>
    fetchApi<import("./types").SourceConfig[]>("/sources"),

  toggleSource: (id: string, enabled: boolean) =>
    fetchApi<import("./types").SourceConfig>(`/sources/${id}`, {
      method: "PATCH",
      body: JSON.stringify({ enabled }),
    }),
};
