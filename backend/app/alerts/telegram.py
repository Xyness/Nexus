import logging
from datetime import datetime, timezone

from telegram import Bot

from app.config import get_settings
from app.models.database import Analysis, NewsItem

logger = logging.getLogger(__name__)

_URGENCY_EMOJI = {
    "breaking": "\U0001F6A8",  # rotating light
    "important": "\u26A0\uFE0F",  # warning
    "normal": "\U0001F4CB",  # clipboard
    "noise": "\U0001F4AD",  # thought bubble
}

_SENTIMENT_EMOJI = {
    "bullish": "\U0001F7E2",  # green circle
    "bearish": "\U0001F534",  # red circle
    "neutral": "\u26AA",  # white circle
}


def _format_relative_time(dt: datetime) -> str:
    """Format a timestamp as relative time."""
    now = datetime.now(timezone.utc)
    diff = now - dt
    seconds = int(diff.total_seconds())
    if seconds < 60:
        return "just now"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours}h ago"
    days = hours // 24
    return f"{days}d ago"


def format_alert_message(analysis: Analysis, news_item: NewsItem) -> str:
    """Format an alert message for Telegram."""
    urgency_emoji = _URGENCY_EMOJI.get(analysis.urgency, "\U0001F4CB")
    sentiment_emoji = _SENTIMENT_EMOJI.get(analysis.sentiment, "\u26AA")
    assets = ", ".join(analysis.affected_assets or []) or "N/A"
    time_str = _format_relative_time(news_item.fetched_at)

    lines = [
        f"{urgency_emoji} *{analysis.urgency.upper()}* | Nexus Alert",
        "",
        f"*{news_item.title}*",
        "",
        f"{sentiment_emoji} Sentiment: *{analysis.sentiment}*",
        f"\U0001F3AF Relevance: *{analysis.relevance_score}/10*",
        f"\U0001F4B0 Assets: {assets}",
        f"\U0001F4DD {analysis.summary}",
        "",
        f"\U0001F517 [Read Article]({news_item.url})",
        f"\U0001F4F0 Source: {news_item.source} | {time_str}",
    ]

    return "\n".join(lines)


async def send_telegram_alert(analysis: Analysis, news_item: NewsItem, chat_id: str):
    """Send a formatted alert to a Telegram chat."""
    settings = get_settings()
    bot = Bot(token=settings.telegram_bot_token)

    message = format_alert_message(analysis, news_item)

    await bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )
    logger.info(f"Telegram alert sent to {chat_id}: {news_item.title[:50]}")
