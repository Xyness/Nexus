import asyncio
import logging

import praw

from app.config import get_settings
from app.models.database import Source
from app.monitors.base import BaseMonitor

logger = logging.getLogger(__name__)

MIN_SCORE = 10  # Minimum upvote score to include


class RedditMonitor(BaseMonitor):
    """Monitor that fetches posts from Reddit subreddits using PRAW."""

    def _get_reddit(self) -> praw.Reddit:
        settings = get_settings()
        return praw.Reddit(
            client_id=settings.reddit_client_id,
            client_secret=settings.reddit_client_secret,
            user_agent="Nexus/2.0 (Financial News Monitor)",
        )

    def _fetch_sync(self, source: Source) -> list[dict]:
        """Synchronous fetch using PRAW."""
        reddit = self._get_reddit()
        # Extract subreddit name from URL
        parts = source.url.rstrip("/").split("/")
        subreddit_name = parts[-1] if parts else source.name

        subreddit = reddit.subreddit(subreddit_name)
        items = []

        for post in subreddit.hot(limit=15):
            if post.score < MIN_SCORE:
                continue
            if post.stickied:
                continue

            items.append({
                "url": f"https://reddit.com{post.permalink}",
                "title": post.title,
                "raw_content": (post.selftext or "")[:5000],
            })

        return items

    async def fetch(self, source: Source) -> list[dict]:
        """Async wrapper around synchronous PRAW calls."""
        try:
            return await asyncio.to_thread(self._fetch_sync, source)
        except Exception as e:
            logger.error(f"Reddit fetch error for {source.name}: {e}")
            return []
