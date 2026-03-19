import pytest
from unittest.mock import MagicMock

from app.monitors.base import BaseMonitor
from app.monitors.mock import MockRSSMonitor, MockRedditMonitor, MockTwitterMonitor


class TestBaseMonitor:
    def test_compute_hash_deterministic(self):
        h1 = BaseMonitor.compute_hash("Test Title", "https://example.com")
        h2 = BaseMonitor.compute_hash("Test Title", "https://example.com")
        assert h1 == h2

    def test_compute_hash_different_inputs(self):
        h1 = BaseMonitor.compute_hash("Title A", "https://example.com/a")
        h2 = BaseMonitor.compute_hash("Title B", "https://example.com/b")
        assert h1 != h2

    def test_compute_hash_case_insensitive(self):
        h1 = BaseMonitor.compute_hash("Test Title", "https://Example.com")
        h2 = BaseMonitor.compute_hash("test title", "https://example.com")
        assert h1 == h2


@pytest.mark.asyncio
class TestMockRSSMonitor:
    async def test_fetch_returns_items(self):
        monitor = MockRSSMonitor()
        source = MagicMock()
        source.name = "CoinDesk"
        source.url = "https://coindesk.com/rss"
        source.type = "rss"

        items = await monitor.fetch(source)
        assert len(items) >= 1
        assert len(items) <= 3

        for item in items:
            assert "url" in item
            assert "title" in item
            assert "raw_content" in item
            assert item["url"].startswith("https://")

    async def test_fetch_generates_unique_urls(self):
        monitor = MockRSSMonitor()
        source = MagicMock()
        source.name = "CoinDesk"
        source.url = "https://coindesk.com/rss"
        source.type = "rss"

        items1 = await monitor.fetch(source)
        items2 = await monitor.fetch(source)
        urls1 = {i["url"] for i in items1}
        urls2 = {i["url"] for i in items2}
        # URLs should differ between fetches (timestamp-based)
        assert urls1 != urls2


@pytest.mark.asyncio
class TestMockRedditMonitor:
    async def test_fetch_returns_items(self):
        monitor = MockRedditMonitor()
        source = MagicMock()
        source.name = "r/CryptoCurrency"
        source.url = "https://reddit.com/r/CryptoCurrency"
        source.type = "reddit"

        items = await monitor.fetch(source)
        assert len(items) >= 1
        for item in items:
            assert "reddit.com" in item["url"]


@pytest.mark.asyncio
class TestMockTwitterMonitor:
    async def test_fetch_returns_items_or_empty(self):
        monitor = MockTwitterMonitor()
        source = MagicMock()
        source.name = "@CoinDesk"
        source.url = "https://x.com/CoinDesk"
        source.type = "twitter"

        items = await monitor.fetch(source)
        assert isinstance(items, list)
        for item in items:
            assert "x.com" in item["url"]
