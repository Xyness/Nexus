import json
import logging
from datetime import datetime, timezone, timedelta

from sqlalchemy import select, func, cast, String

from app.agent.state import NewsAnalysisResult
from app.api.news import broadcast_event
from app.config import Settings, get_settings
from app.db.session import async_session_factory
from app.models.database import Alert, Analysis, NewsItem, Watchlist

logger = logging.getLogger(__name__)

# Cooldown: 30 minutes per asset
COOLDOWN_MINUTES = 30


async def _is_on_cooldown(asset: str) -> bool:
    """Check if an asset is on alert cooldown."""
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=COOLDOWN_MINUTES)
    async with async_session_factory() as session:
        result = await session.execute(
            select(func.count(Alert.id))
            .join(Analysis, Alert.analysis_id == Analysis.id)
            .where(
                Alert.sent_at >= cutoff,
                cast(Analysis.affected_assets, String).contains(asset),
            )
        )
        count = result.scalar() or 0
        return count > 0


async def _get_watchlist_assets() -> dict[str, float]:
    """Get watchlist assets with their thresholds."""
    async with async_session_factory() as session:
        result = await session.execute(select(Watchlist))
        items = result.scalars().all()
        return {item.asset_symbol: item.alert_threshold for item in items}


async def should_alert(result: NewsAnalysisResult, settings: Settings) -> bool:
    """Determine if an analysis result should trigger an alert.

    Rules:
    - score >= 7 AND urgency >= important → alert
    - score >= asset's watchlist threshold if asset is in watchlist → alert
    - Anti-spam: cooldown 30min per asset
    """
    score = result["relevance_score"]
    urgency = result["urgency"]
    assets = result["affected_assets"]

    # Check watchlist first (lower threshold)
    watchlist = await _get_watchlist_assets()
    for asset in assets:
        if asset in watchlist:
            threshold = watchlist[asset]
            if score >= threshold:
                # Check cooldown
                if not await _is_on_cooldown(asset):
                    return True

    # Standard threshold: high relevance + urgency
    if score >= settings.alert_relevance_threshold and urgency in ("breaking", "important"):
        # Check cooldown for any affected asset
        for asset in assets:
            if not await _is_on_cooldown(asset):
                return True

    return False


async def send_alert(analysis: Analysis, news_item: NewsItem):
    """Send alert for an analysis result."""
    settings = get_settings()

    # Get or create telegram sender
    if settings.telegram_enabled:
        from app.alerts.telegram import send_telegram_alert
        for chat_id in settings.chat_id_list:
            try:
                await send_telegram_alert(analysis, news_item, chat_id)
                await _record_alert(analysis.id, "telegram", chat_id)
            except Exception as e:
                logger.error(f"Failed to send Telegram alert to {chat_id}: {e}")
    else:
        # Mock mode: log to console
        from app.alerts.mock import log_mock_alert
        await log_mock_alert(analysis, news_item)
        await _record_alert(analysis.id, "console", "mock")

    # Broadcast SSE event
    event_data = json.dumps({
        "analysis_id": analysis.id,
        "title": news_item.title,
        "sentiment": analysis.sentiment,
        "urgency": analysis.urgency,
        "relevance_score": analysis.relevance_score,
        "affected_assets": analysis.affected_assets,
    })
    await broadcast_event("alert_sent", event_data)


async def _record_alert(analysis_id: str, channel: str, recipient: str):
    """Record an alert in the database."""
    async with async_session_factory() as session:
        alert = Alert(
            analysis_id=analysis_id,
            channel=channel,
            recipient=recipient,
        )
        session.add(alert)
        await session.commit()
    logger.info(f"Alert recorded: analysis={analysis_id}, channel={channel}, recipient={recipient}")
