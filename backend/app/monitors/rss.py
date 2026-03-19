import asyncio
import logging

import feedparser

from app.models.database import Source
from app.monitors.base import BaseMonitor

logger = logging.getLogger(__name__)


class RSSMonitor(BaseMonitor):
    """Monitor that fetches news from RSS feeds."""

    async def fetch(self, source: Source) -> list[dict]:
        """Parse RSS feed and return news items."""
        feed = await asyncio.to_thread(feedparser.parse, source.url)

        if feed.bozo and not feed.entries:
            logger.warning(f"RSS feed error for {source.name}: {feed.bozo_exception}")
            return []

        items = []
        for entry in feed.entries[:20]:  # Limit to 20 most recent
            url = entry.get("link", "")
            title = entry.get("title", "")
            if not url or not title:
                continue

            # Extract content from various RSS fields
            raw_content = ""
            if entry.get("summary"):
                raw_content = entry.summary
            elif entry.get("description"):
                raw_content = entry.description
            elif entry.get("content"):
                raw_content = entry.content[0].get("value", "") if entry.content else ""

            items.append({
                "url": url,
                "title": title,
                "raw_content": raw_content[:5000],  # Limit content size
            })

        return items
