export interface ReportSummary {
  id: string;
  topic: string;
  status: "pending" | "running" | "completed" | "error";
  sentiment: string | null;
  sentiment_score: number | null;
  sources_count: number;
  created_at: string;
  completed_at: string | null;
}

export interface SourceItem {
  title: string;
  url: string;
}

export interface ReportDetail extends ReportSummary {
  content_md: string | null;
  sub_questions: string[] | null;
  sources: SourceItem[] | null;
  error_message: string | null;
}

export interface WatchResponse {
  report_id: string;
  status: string;
}

export interface Schedule {
  id: string;
  topic: string;
  cron_expression: string;
  is_active: boolean;
  last_run_at: string | null;
  created_at: string;
}
