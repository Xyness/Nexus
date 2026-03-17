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
};
