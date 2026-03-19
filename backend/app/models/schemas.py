from pydantic import BaseModel
from datetime import datetime


# --- Watch ---

class WatchRequest(BaseModel):
    topic: str


class WatchResponse(BaseModel):
    report_id: str
    status: str


# --- Reports ---

class ReportSummary(BaseModel):
    id: str
    topic: str
    status: str
    sentiment: str | None = None
    sentiment_score: float | None = None
    sources_count: int = 0
    created_at: datetime
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}


class SourceItem(BaseModel):
    title: str
    url: str


class ReportDetail(ReportSummary):
    content_md: str | None = None
    sub_questions: list[str] | None = None
    sources: list[SourceItem] | None = None
    error_message: str | None = None

    model_config = {"from_attributes": True}


# --- Schedule ---

class ScheduleCreateRequest(BaseModel):
    topic: str
    cron_expression: str


class ScheduleResponse(BaseModel):
    id: str
    topic: str
    cron_expression: str
    is_active: bool
    last_run_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


# --- News ---

class NewsItemResponse(BaseModel):
    id: str
    url: str
    title: str
    source: str
    source_type: str
    raw_content: str | None = None
    fetched_at: datetime
    status: str

    model_config = {"from_attributes": True}


class NewsItemWithAnalysis(BaseModel):
    id: str
    url: str
    title: str
    source: str
    source_type: str
    fetched_at: datetime
    status: str
    analysis: "AnalysisResponse | None" = None

    model_config = {"from_attributes": True}


class AnalysisResponse(BaseModel):
    id: str
    news_item_id: str
    affected_assets: list[str] | None = None
    sentiment: str | None = None
    urgency: str | None = None
    relevance_score: float = 0.0
    confidence: float = 0.0
    summary: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Alerts ---

class AlertResponse(BaseModel):
    id: str
    analysis_id: str
    sent_at: datetime
    channel: str
    recipient: str
    analysis: AnalysisResponse | None = None

    model_config = {"from_attributes": True}


# --- Watchlist ---

class WatchlistItemCreate(BaseModel):
    asset_symbol: str
    alert_threshold: float = 5.0


class WatchlistItemResponse(BaseModel):
    id: str
    asset_symbol: str
    alert_threshold: float
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Sources ---

class SourceResponse(BaseModel):
    id: str
    name: str
    type: str
    url: str
    enabled: bool
    last_fetched: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class SourceToggleRequest(BaseModel):
    enabled: bool


# --- Stats ---

class DailyStatsResponse(BaseModel):
    total_news: int = 0
    analyzed_news: int = 0
    alerts_sent: int = 0
    bullish_count: int = 0
    bearish_count: int = 0
    neutral_count: int = 0
    active_sources: int = 0
