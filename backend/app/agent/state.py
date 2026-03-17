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
