import hashlib
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone

from sqlalchemy import select

from app.db.session import async_session_factory
from app.models.database import NewsItem, Source

logger = logging.getLogger(__name__)


class BaseMonitor(ABC):
    """Abstract base class for news monitors."""

    @abstractmethod
    async def fetch(self, source: Source) -> list[dict]:
        """Fetch news items from a source.

        Returns list of dicts with keys: url, title, raw_content
        """
        ...

    @staticmethod
    def compute_hash(title: str, url: str) -> str:
        """Compute SHA-256 hash for deduplication."""
        content = f"{title.strip().lower()}|{url.strip().lower()}"
        return hashlib.sha256(content.encode()).hexdigest()

    async def run(self, source: Source) -> list[NewsItem]:
        """Fetch, deduplicate, and persist news items."""
        try:
            raw_items = await self.fetch(source)
        except Exception as e:
            logger.error(f"Error fetching from {source.name}: {e}")
            return []

        new_items = []
        async with async_session_factory() as session:
            for item in raw_items:
                content_hash = self.compute_hash(item["title"], item["url"])

                # Check for duplicate
                existing = await session.execute(
                    select(NewsItem).where(NewsItem.content_hash == content_hash)
                )
                if existing.scalar_one_or_none():
                    continue

                news_item = NewsItem(
                    url=item["url"],
                    title=item["title"],
                    source=source.name,
                    source_type=source.type,
                    raw_content=item.get("raw_content", ""),
                    content_hash=content_hash,
                    fetched_at=datetime.now(timezone.utc),
                    status="pending",
                )
                session.add(news_item)
                new_items.append(news_item)

            if new_items:
                await session.commit()
                for item in new_items:
                    await session.refresh(item)

            # Update source last_fetched
            src = await session.get(Source, source.id)
            if src:
                src.last_fetched = datetime.now(timezone.utc)
                await session.commit()

        if new_items:
            logger.info(f"Fetched {len(new_items)} new items from {source.name}")
        return new_items
