import asyncio
import logging

import tweepy

from app.config import get_settings
from app.models.database import Source
from app.monitors.base import BaseMonitor

logger = logging.getLogger(__name__)


class TwitterMonitor(BaseMonitor):
    """Monitor that fetches tweets using Twitter/X API v2 via Tweepy."""

    def _get_client(self) -> tweepy.Client:
        settings = get_settings()
        return tweepy.Client(bearer_token=settings.twitter_bearer_token)

    def _fetch_sync(self, source: Source) -> list[dict]:
        """Synchronous fetch using Tweepy."""
        client = self._get_client()

        # Extract username from URL
        parts = source.url.rstrip("/").split("/")
        username = parts[-1].lstrip("@")

        # Get user ID
        user = client.get_user(username=username)
        if not user.data:
            logger.warning(f"Twitter user not found: {username}")
            return []

        # Get recent tweets
        tweets = client.get_users_tweets(
            id=user.data.id,
            max_results=10,
            tweet_fields=["created_at", "public_metrics"],
        )

        if not tweets.data:
            return []

        items = []
        for tweet in tweets.data:
            items.append({
                "url": f"https://x.com/{username}/status/{tweet.id}",
                "title": tweet.text[:200],
                "raw_content": tweet.text,
            })

        return items

    async def fetch(self, source: Source) -> list[dict]:
        """Async wrapper around synchronous Tweepy calls."""
        try:
            return await asyncio.to_thread(self._fetch_sync, source)
        except Exception as e:
            logger.error(f"Twitter fetch error for {source.name}: {e}")
            return []
