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
