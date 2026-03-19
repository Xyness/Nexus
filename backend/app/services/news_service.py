import logging

from sqlalchemy import select

from app.db.session import async_session_factory
from app.models.database import NewsItem

logger = logging.getLogger(__name__)


async def get_pending_news() -> list[NewsItem]:
    """Get all pending news items awaiting analysis."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(NewsItem)
            .where(NewsItem.status == "pending")
            .order_by(NewsItem.fetched_at.asc())
        )
        return list(result.scalars().all())


async def update_status(news_item_id: str, status: str):
    """Update the status of a news item."""
    async with async_session_factory() as session:
        item = await session.get(NewsItem, news_item_id)
        if item:
            item.status = status
            await session.commit()


async def get_recent_news(limit: int = 50) -> list[NewsItem]:
    """Get the most recent news items."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(NewsItem)
            .order_by(NewsItem.fetched_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
