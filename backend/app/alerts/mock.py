import logging

from app.models.database import Analysis, NewsItem

logger = logging.getLogger(__name__)


async def log_mock_alert(analysis: Analysis, news_item: NewsItem):
    """Log an alert to console instead of sending to Telegram."""
    assets = ", ".join(analysis.affected_assets or [])
    logger.info(
        f"\U0001F514 MOCK ALERT | "
        f"{analysis.urgency.upper()} | "
        f"Score: {analysis.relevance_score}/10 | "
        f"Sentiment: {analysis.sentiment} | "
        f"Assets: {assets} | "
        f"Title: {news_item.title[:80]}"
    )
