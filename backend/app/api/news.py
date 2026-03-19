import asyncio
import logging
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select, func

from app.db.session import async_session_factory
from app.models.database import NewsItem, Analysis, Alert, Source
from app.models.schemas import NewsItemWithAnalysis, AnalysisResponse, DailyStatsResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/news", tags=["news"])

# SSE clients
_sse_queues: list[asyncio.Queue] = []


async def broadcast_event(event_type: str, data: str):
    """Broadcast an SSE event to all connected clients."""
    message = f"event: {event_type}\ndata: {data}\n\n"
    dead_queues = []
    for q in _sse_queues:
        try:
            q.put_nowait(message)
        except asyncio.QueueFull:
            dead_queues.append(q)
    for q in dead_queues:
        _sse_queues.remove(q)


async def _sse_generator(queue: asyncio.Queue):
    """Generate SSE events for a client."""
    try:
        while True:
            try:
                message = await asyncio.wait_for(queue.get(), timeout=30)
                yield message
            except asyncio.TimeoutError:
                yield ": keepalive\n\n"
    except asyncio.CancelledError:
        pass
    finally:
        if queue in _sse_queues:
            _sse_queues.remove(queue)


@router.get("/stream")
async def news_stream():
    """SSE endpoint for real-time news updates."""
    queue: asyncio.Queue = asyncio.Queue(maxsize=200)
    _sse_queues.append(queue)
    return StreamingResponse(
        _sse_generator(queue),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@router.get("", response_model=list[NewsItemWithAnalysis])
async def get_news(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Get recent news items with their analyses."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(NewsItem)
            .order_by(NewsItem.fetched_at.desc())
            .offset(offset)
            .limit(limit)
        )
        news_items = result.scalars().all()

        response = []
        for item in news_items:
            # Get latest analysis for this news item
            analysis_result = await session.execute(
                select(Analysis)
                .where(Analysis.news_item_id == item.id)
                .order_by(Analysis.created_at.desc())
                .limit(1)
            )
            analysis = analysis_result.scalar_one_or_none()

            analysis_resp = None
            if analysis:
                analysis_resp = AnalysisResponse(
                    id=analysis.id,
                    news_item_id=analysis.news_item_id,
                    affected_assets=analysis.affected_assets,
                    sentiment=analysis.sentiment,
                    urgency=analysis.urgency,
                    relevance_score=analysis.relevance_score,
                    confidence=analysis.confidence,
                    summary=analysis.summary,
                    created_at=analysis.created_at,
                )

            response.append(NewsItemWithAnalysis(
                id=item.id,
                url=item.url,
                title=item.title,
                source=item.source,
                source_type=item.source_type,
                fetched_at=item.fetched_at,
                status=item.status,
                analysis=analysis_resp,
            ))

        return response


@router.get("/stats/daily", response_model=DailyStatsResponse)
async def get_daily_stats():
    """Get daily statistics."""
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

    async with async_session_factory() as session:
        # Total news today
        total_news = await session.execute(
            select(func.count(NewsItem.id)).where(NewsItem.fetched_at >= today_start)
        )
        total = total_news.scalar() or 0

        # Analyzed news today
        analyzed = await session.execute(
            select(func.count(NewsItem.id)).where(
                NewsItem.fetched_at >= today_start,
                NewsItem.status == "analyzed",
            )
        )
        analyzed_count = analyzed.scalar() or 0

        # Alerts today
        alerts_count_result = await session.execute(
            select(func.count(Alert.id)).where(Alert.sent_at >= today_start)
        )
        alerts_count = alerts_count_result.scalar() or 0

        # Sentiment counts today
        sentiment_results = await session.execute(
            select(Analysis.sentiment, func.count(Analysis.id))
            .where(Analysis.created_at >= today_start)
            .group_by(Analysis.sentiment)
        )
        sentiment_counts = {row[0]: row[1] for row in sentiment_results.all()}

        # Active sources
        active_sources = await session.execute(
            select(func.count(Source.id)).where(Source.enabled.is_(True))
        )
        active_count = active_sources.scalar() or 0

        return DailyStatsResponse(
            total_news=total,
            analyzed_news=analyzed_count,
            alerts_sent=alerts_count,
            bullish_count=sentiment_counts.get("bullish", 0),
            bearish_count=sentiment_counts.get("bearish", 0),
            neutral_count=sentiment_counts.get("neutral", 0),
            active_sources=active_count,
        )
