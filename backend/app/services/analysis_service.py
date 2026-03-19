import json
import logging

from sqlalchemy import select

from app.agent.analyzer import analyze_news_item
from app.api.news import broadcast_event
from app.config import get_settings
from app.db.session import async_session_factory
from app.models.database import NewsItem, Analysis, Watchlist
from app.services.alert_service import should_alert, send_alert
from app.services.news_service import get_pending_news, update_status

logger = logging.getLogger(__name__)


async def process_pending_news():
    """Process all pending news items through the analysis pipeline."""
    pending = await get_pending_news()
    if not pending:
        return

    logger.info(f"Processing {len(pending)} pending news items")

    for item in pending:
        try:
            result = await analyze_news_item(
                title=item.title,
                source=item.source,
                content=item.raw_content or "",
            )

            # Persist analysis
            async with async_session_factory() as session:
                analysis = Analysis(
                    news_item_id=item.id,
                    affected_assets=result["affected_assets"],
                    sentiment=result["sentiment"],
                    urgency=result["urgency"],
                    relevance_score=result["relevance_score"],
                    confidence=result["confidence"],
                    summary=result["summary"],
                )
                session.add(analysis)
                await session.commit()
                await session.refresh(analysis)

            await update_status(item.id, "analyzed")

            # Broadcast SSE event
            event_data = json.dumps({
                "news_id": item.id,
                "title": item.title,
                "source": item.source,
                "relevance_score": result["relevance_score"],
                "sentiment": result["sentiment"],
                "urgency": result["urgency"],
                "summary": result["summary"],
                "affected_assets": result["affected_assets"],
            })
            await broadcast_event("news_analyzed", event_data)

            # Check if we should alert
            settings = get_settings()
            if await should_alert(result, settings):
                await send_alert(analysis, item)

            logger.info(
                f"Analyzed: '{item.title[:60]}...' — "
                f"score={result['relevance_score']}, "
                f"sentiment={result['sentiment']}, "
                f"urgency={result['urgency']}"
            )

        except Exception as e:
            logger.error(f"Error analyzing news item {item.id}: {e}")
            await update_status(item.id, "error")
