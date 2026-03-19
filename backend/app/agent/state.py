import operator
from typing import Annotated, TypedDict


class AgentState(TypedDict):
    topic: str
    sub_questions: list[str]
    search_results: Annotated[list[dict], operator.add]
    summaries: list[str]
    sentiment: str
    sentiment_score: float
    key_facts: list[str]
    report_md: str
    errors: Annotated[list[str], operator.add]


class NewsAnalysisResult(TypedDict):
    relevance_score: float  # 0-10
    affected_assets: list[str]
    sentiment: str  # bullish, bearish, neutral
    urgency: str  # breaking, important, normal, noise
    summary: str
    confidence: float  # 0-1
