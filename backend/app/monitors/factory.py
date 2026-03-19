from app.config import get_settings
from app.monitors.base import BaseMonitor


def get_monitor(source_type: str) -> BaseMonitor:
    """Factory to get the appropriate monitor for a source type.

    Returns mock monitors in mock mode, real monitors otherwise.
    """
    settings = get_settings()

    if source_type == "rss":
        if settings.mock_mode:
            from app.monitors.mock import MockRSSMonitor
            return MockRSSMonitor()
        from app.monitors.rss import RSSMonitor
        return RSSMonitor()

    elif source_type == "reddit":
        if settings.mock_mode or not settings.reddit_enabled:
            from app.monitors.mock import MockRedditMonitor
            return MockRedditMonitor()
        from app.monitors.reddit import RedditMonitor
        return RedditMonitor()

    elif source_type == "twitter":
        if settings.mock_mode or not settings.twitter_enabled:
            from app.monitors.mock import MockTwitterMonitor
            return MockTwitterMonitor()
        from app.monitors.twitter import TwitterMonitor
        return TwitterMonitor()

    else:
        raise ValueError(f"Unknown source type: {source_type}")
