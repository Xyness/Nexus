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

// --- Nexus types ---

export interface AnalysisResponse {
  id: string;
  news_item_id: string;
  affected_assets: string[] | null;
  sentiment: string | null;
  urgency: string | null;
  relevance_score: number;
  confidence: number;
  summary: string | null;
  created_at: string;
}

export interface NewsItemWithAnalysis {
  id: string;
  url: string;
  title: string;
  source: string;
  source_type: string;
  fetched_at: string;
  status: string;
  analysis: AnalysisResponse | null;
}

export interface AlertResponse {
  id: string;
  analysis_id: string;
  sent_at: string;
  channel: string;
  recipient: string;
  analysis: AnalysisResponse | null;
}

export interface DailyStatsResponse {
  total_news: number;
  analyzed_news: number;
  alerts_sent: number;
  bullish_count: number;
  bearish_count: number;
  neutral_count: number;
  active_sources: number;
}

export interface WatchlistItem {
  id: string;
  asset_symbol: string;
  alert_threshold: number;
  created_at: string;
}

export interface SourceConfig {
  id: string;
  name: string;
  type: string;
  url: string;
  enabled: boolean;
  last_fetched: string | null;
  created_at: string;
}
